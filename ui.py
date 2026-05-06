import uuid
import streamlit as st
from dotenv import load_dotenv
from graph.workflow import build_graph
load_dotenv()
st.set_page_config(page_title="Production Incident AI Agent", layout="wide")

st.title("🚨 Production Incident AI Agent")
st.caption("LangGraph + Ollama + Streamlit | Production Debugging Demo")

service_name = st.selectbox(
    "Select incident scenario",
    [
        "payment-api",
        "order-api",
        "auth-service",
        "inventory-service",
        "deployment-service",
    ],
)

query = st.text_input(
    "Ask incident question",
    f"Why is {service_name} failing?"
)

if st.button("Analyze Incident", type="primary"):
    app = build_graph()
    trace_id = str(uuid.uuid4())[:8]

    initial_state = {
        "user_question": query,
        "service_name": service_name,
        "logs": [],
        "error_type": None,
        "severity": None,
        "sla_impact": None,
        "circuit_breaker_status": None,
        "recommended_owner": None,
        "root_cause": None,
        "fix_recommendation": None,
        "confidence_score": 0.0,
        "requires_human": False,
        "trace": [],
    }

    with st.spinner("Running LangGraph incident agents..."):
        result = app.invoke(initial_state)

    st.subheader("Production Incident Summary")

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Trace ID", trace_id)
    m2.metric("Severity", result["severity"])
    m3.metric("Error Type", result["error_type"])
    m4.metric("Confidence", result["confidence_score"])
    m5.metric("Human Review", "Yes" if result["requires_human"] else "No")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Root Cause")
        st.write(result["root_cause"])

        st.subheader("Fix Recommendation")
        st.write(result["fix_recommendation"])

    with col2:
        st.subheader("SLA / Ownership")
        st.info(f"**SLA Impact:** {result['sla_impact']}")
        st.warning(f"**Circuit Breaker:** {result['circuit_breaker_status']}")
        st.success(f"**Recommended Owner:** {result['recommended_owner']}")

        st.subheader("Agent Workflow")

        agent_order = [
            ("log_collector", "1. Log Collector Agent"),
            ("error_classifier", "2. Error Classification Agent"),
            ("severity_analyzer", "3. Severity Analyzer Agent"),
            ("similar_incident_retrieval", "4. Similar Incident Retrieval Agent"),
            ("root_cause", "5. Root Cause Agent"),
            ("fix_recommendation", "6. Fix Recommendation Agent"),
            ("human_review", "7. Human Approval Agent"),
        ]

        completed_nodes = [step["node"] for step in result["trace"]]

        for node_key, label in agent_order:
            if node_key in completed_nodes:
                st.success(f"✅ {label}")
            else:
                st.info(f"⏳ {label} - Not executed yet")

        st.subheader("Detailed Trace")
        for step in result["trace"]:
            st.json(step)

    st.subheader("Logs Used")
    for log in result["logs"]:
        st.code(log)