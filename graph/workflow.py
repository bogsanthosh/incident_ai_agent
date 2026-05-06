from langgraph.graph import StateGraph, END
from graph.state import IncidentState
from graph.nodes import (
    log_collector_node,
    error_classifier_node,
    severity_node,
    root_cause_node,
    fix_recommendation_node,
    human_review_node,
)


def should_escalate(state: IncidentState):
    if state["requires_human"]:
        return "human_review"
    return "end"


def build_graph():
    graph = StateGraph(IncidentState)

    graph.add_node("log_collector", log_collector_node)
    graph.add_node("error_classifier", error_classifier_node)
    graph.add_node("severity_analyzer", severity_node)
    graph.add_node("root_cause", root_cause_node)
    graph.add_node("fix_recommendation", fix_recommendation_node)
    graph.add_node("human_review", human_review_node)

    graph.set_entry_point("log_collector")

    graph.add_edge("log_collector", "error_classifier")
    graph.add_edge("error_classifier", "severity_analyzer")
    graph.add_edge("severity_analyzer", "root_cause")
    graph.add_edge("root_cause", "fix_recommendation")

    graph.add_conditional_edges(
        "fix_recommendation",
        should_escalate,
        {
            "human_review": "human_review",
            "end": END,
        },
    )

    graph.add_edge("human_review", END)

    return graph.compile()