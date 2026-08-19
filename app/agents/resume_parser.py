from langchain_core.messages import HumanMessage, SystemMessage

from app.core.llm import get_llm
from app.schemas.models import ResumeSkills

SYSTEM_PROMPT = """You are a technical recruiter analyzing a candidate's resume.

Extract every skill the candidate has, whether listed explicitly (e.g. in a \
Skills section) or demonstrated through work experience, projects, or \
education, and classify each one into exactly one of these categories:
- technical_skills: programming languages, CS fundamentals, technical concepts \
(e.g. "Python", "distributed systems", "REST API design")
- tools_and_frameworks: named tools, libraries, platforms, frameworks, cloud \
services, databases (e.g. "React", "Docker", "PostgreSQL", "AWS")
- soft_skills: communication, collaboration, leadership, and similar \
non-technical abilities

Do not invent skills that are not stated or clearly implied by the text."""


def parse_resume(resume_text: str) -> ResumeSkills:
    llm = get_llm(temperature=0.0).with_structured_output(ResumeSkills)
    return llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=resume_text),
        ]
    )
