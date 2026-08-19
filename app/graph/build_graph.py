from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.agents.gap_analyzer import analyze_gap
from app.agents.jd_parser import parse_jd
from app.agents.resume_parser import parse_resume
from app.agents.roadmap import build_roadmap
from app.schemas.models import GapAnalysis, JDSkills, ResumeSkills, Roadmap


class GraphState(TypedDict):
    job_description: str
    resume_text: str
    jd_skills: JDSkills
    resume_skills: ResumeSkills
    gap_analysis: GapAnalysis
    roadmap: Roadmap


def _jd_parser_node(state: GraphState) -> dict:
    return {"jd_skills": parse_jd(state["job_description"])}


def _resume_parser_node(state: GraphState) -> dict:
    return {"resume_skills": parse_resume(state["resume_text"])}


def _gap_analyzer_node(state: GraphState) -> dict:
    return {"gap_analysis": analyze_gap(state["jd_skills"], state["resume_skills"])}


def _roadmap_node(state: GraphState) -> dict:
    return {"roadmap": build_roadmap(state["gap_analysis"])}


def build_graph() -> CompiledStateGraph:
    graph = StateGraph(GraphState)
    graph.add_node("jd_parser", _jd_parser_node)
    graph.add_node("resume_parser", _resume_parser_node)
    graph.add_node("gap_analyzer", _gap_analyzer_node)
    graph.add_node("roadmap", _roadmap_node)

    graph.add_edge(START, "jd_parser")
    graph.add_edge(START, "resume_parser")
    graph.add_edge("jd_parser", "gap_analyzer")
    graph.add_edge("resume_parser", "gap_analyzer")
    graph.add_edge("gap_analyzer", "roadmap")
    graph.add_edge("roadmap", END)

    return graph.compile()


compiled_graph = build_graph()
