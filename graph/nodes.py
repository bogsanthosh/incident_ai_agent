from langchain_ollama import ChatOllama
from tools.mock_logs import get_mock_logs
from tools.databricks_logs import fetch_logs_from_databricks

llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0,
    num_ctx=1024,
    num_predict=300
)                                    


def log_collector_node(state):
    service_name = state.get("service_name") or "payment-api"

    source = "unknown"
    logs = []

    try:
        logs = fetch_logs_from_databricks(service_name)

        if logs:
            source = "databricks"
        else:
            logs = get_mock_logs(service_name)
            source = "mock_fallback_no_databricks_logs"

    except Exception as e:
        logs = get_mock_logs(service_name)
        source = f"mock_fallback_due_to_error: {str(e)}"

    state["logs"] = logs
    state["trace"].append({
        "node": "log_collector",
        "status": "success",
        "source": source,
        "service_name": service_name,
        "log_count": len(logs)
    })

    return state


def error_classifier_node(state):
    logs_text = "\n".join(state["logs"])

    prompt = f"""
Classify this production incident.

Logs:
{logs_text}

Return only one:
downstream_503, timeout, auth_failure, database_issue, memory_issue, deployment_failure, unknown
"""

    response = llm.invoke(prompt)
    raw_output = response.content.strip().lower()

    valid_types = [
        "downstream_503",
        "timeout",
        "auth_failure",
        "database_issue",
        "memory_issue",
        "deployment_failure",
        "unknown"
    ]

    error_type = "unknown"

    for item in valid_types:
        if item in raw_output:
            error_type = item
            break

    state["error_type"] = error_type
    state["trace"].append({
        "node": "error_classifier",
        "status": "success",
        "error_type": error_type
    })
    return state


def severity_node(state):
    logs_text = "\n".join(state["logs"]).lower()
    error_type = state.get("error_type", "unknown")

    severity = "Medium"
    sla_impact = "Partial degradation"
    circuit_breaker_status = "Not triggered"
    recommended_owner = "Platform Support"

    if "503" in logs_text or "circuit breaker" in logs_text:
        severity = "High"
        sla_impact = "Payment/API transaction failures likely"
        circuit_breaker_status = "Opened"
        recommended_owner = "Backend/API Team"

    elif "database" in logs_text or "connection pool" in logs_text:
        severity = "High"
        sla_impact = "Order processing latency or failure"
        circuit_breaker_status = "Recommended"
        recommended_owner = "Database/SRE Team"

    elif "jwt" in logs_text or "token" in logs_text:
        severity = "High"
        sla_impact = "Login/authentication failures"
        circuit_breaker_status = "Not applicable"
        recommended_owner = "Identity/Auth Team"

    elif "oomkilled" in logs_text or "memory" in logs_text:
        severity = "Critical"
        sla_impact = "Service restart / availability risk"
        circuit_breaker_status = "Recommended"
        recommended_owner = "Platform/Kubernetes Team"

    elif "deployment" in logs_text or "rollback" in logs_text:
        severity = "Medium"
        sla_impact = "New release failed; rollback active"
        circuit_breaker_status = "Not applicable"
        recommended_owner = "DevOps/Release Team"

    confidence = 0.85 if severity in ["High", "Critical"] else 0.75

    state["severity"] = severity
    state["sla_impact"] = sla_impact
    state["circuit_breaker_status"] = circuit_breaker_status
    state["recommended_owner"] = recommended_owner
    state["confidence_score"] = confidence
    state["requires_human"] = severity == "Critical"

    state["trace"].append({
        "node": "severity_analyzer",
        "status": "success",
        "severity": severity,
        "sla_impact": sla_impact,
        "recommended_owner": recommended_owner
    })

    return state


def root_cause_node(state):
    logs_text = "\n".join(state["logs"])

    prompt = f"""
You are a senior production support engineer.

User question:
{state["user_question"]}

Error type:
{state["error_type"]}

Severity:
{state["severity"]}

Logs:
{logs_text}

Explain:
1. What failed
2. Most likely root cause
3. Business impact
"""

    response = llm.invoke(prompt)

    state["root_cause"] = response.content
    state["trace"].append({
        "node": "root_cause",
        "status": "success"
    })
    return state


def fix_recommendation_node(state):
    prompt = f"""
Based on this root cause, recommend production-safe fixes.

Root cause:
{state["root_cause"]}

Incident metadata:
- Severity: {state["severity"]}
- SLA Impact: {state["sla_impact"]}
- Circuit Breaker Status: {state["circuit_breaker_status"]}
- Recommended Owner: {state["recommended_owner"]}

Include:
1. Immediate mitigation
2. Long-term fix
3. Monitoring improvement
4. Circuit breaker recommendation
"""

    response = llm.invoke(prompt)

    state["fix_recommendation"] = response.content

    state["trace"].append({
        "node": "fix_recommendation",
        "status": "success",
        "confidence_score": state["confidence_score"]
    })
    return state


def human_review_node(state):
    state["trace"].append({
        "node": "human_review",
        "status": "required",
        "reason": "Critical severity requires human approval"
    })
    return state