from typing import TypedDict, List, Dict, Any, Optional


class IncidentState(TypedDict):
    user_question: str
    service_name: Optional[str]
    logs: List[str]
    error_type: Optional[str]
    severity: Optional[str]
    sla_impact: Optional[str]
    circuit_breaker_status: Optional[str]
    recommended_owner: Optional[str]
    root_cause: Optional[str]
    fix_recommendation: Optional[str]
    confidence_score: float
    requires_human: bool
    trace: List[Dict[str, Any]]