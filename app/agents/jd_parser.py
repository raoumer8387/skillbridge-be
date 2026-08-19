from langchain_core.messages import HumanMessage, SystemMessage

from app.core.llm import get_llm
from app.schemas.models import JDSkills

SYSTEM_PROMPT = """You are a technical recruiter analyzing a job description.

Extract every skill mentioned or clearly implied in the job description and \
classify each one into exactly one of these categories:
- technical_skills: programming languages, CS fundamentals, technical concepts \
(e.g. "Python", "distributed systems", "REST API design")
- tools_and_frameworks: named tools, libraries, platforms, frameworks, cloud \
services, databases (e.g. "React", "Docker", "PostgreSQL", "AWS")
- soft_skills: communication, collaboration, leadership, and similar \
non-technical abilities

Within each category, split skills into:
- required: explicitly stated as required, must-have, or a core responsibility
- preferred: explicitly stated as preferred, nice-to-have, or a bonus

If the job description does not distinguish required from preferred for a \
skill, classify it as required. Do not invent skills that are not stated or \
clearly implied by the text."""


def parse_jd(jd_text: str) -> JDSkills:
    llm = get_llm(temperature=0.0).with_structured_output(JDSkills)
    return llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=jd_text),
        ]
    )
