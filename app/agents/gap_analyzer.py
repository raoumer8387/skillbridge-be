import json

from langchain_core.messages import HumanMessage, SystemMessage

from app.core.llm import get_llm
from app.schemas.models import GapAnalysis, JDSkills, ResumeSkills

SYSTEM_PROMPT = """You compare a job description's required skills against a \
candidate's resume skills to find gaps, one category at a time \
(technical_skills, tools_and_frameworks, soft_skills).

You will receive two JSON objects: "jd_skills" (with "required" and \
"preferred" skills per category) and "resume_skills" (a flat list of skills \
per category).

For each category, decide for every JD skill (both required and preferred) \
whether the candidate has an equivalent skill in their resume. Treat two \
skills as equivalent if they refer to the same underlying technology or \
ability even when worded differently — abbreviations, aliases, casing, or \
minor phrasing differences (e.g. "Postgres" and "PostgreSQL", "JS" and \
"JavaScript" are equivalent). Do not treat genuinely different skills as \
equivalent just because they are related (e.g. "Docker" and "Kubernetes" are \
NOT equivalent).

For each category, produce:
- matched: JD skills (required or preferred) that have an equivalent resume \
skill. Use the JD's own wording for each matched skill, not the resume's.
- missing_required: JD "required" skills with no equivalent in the resume
- missing_preferred: JD "preferred" skills with no equivalent in the resume

Every JD skill must end up in exactly one of matched, missing_required, or \
missing_preferred. Ignore resume skills that have no corresponding JD skill — \
this is a gap analysis against the JD, not a resume summary."""


def analyze_gap(jd_skills: JDSkills, resume_skills: ResumeSkills) -> GapAnalysis:
    llm = get_llm(temperature=0.0).with_structured_output(GapAnalysis)
    payload = json.dumps(
        {
            "jd_skills": jd_skills.model_dump(),
            "resume_skills": resume_skills.model_dump(),
        },
        indent=2,
    )
    return llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=payload),
        ]
    )
