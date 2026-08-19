import json

from langchain_core.messages import HumanMessage, SystemMessage

from app.core.llm import get_llm
from app.schemas.models import GapAnalysis, Roadmap

SYSTEM_PROMPT = """You turn a skill gap analysis into a roadmap of concrete, \
buildable projects — one per missing skill. Each suggestion must be \
something a student could actually build or complete and put on their \
resume or GitHub. NEVER suggest a course, tutorial, book, certification, or \
mock interview question — those are not projects.

You will receive a JSON list called "skills_to_cover". Each entry already \
has its "skill", "category", and "priority" assigned. Generate exactly one \
roadmap item per entry in this list — no more, no fewer — reusing that \
entry's skill, category, and priority exactly as given. Do not invent \
additional skills or omit any entry.

For technical_skills and tools_and_frameworks gaps, propose a specific \
coding project scoped tightly enough to start immediately — name the \
concrete thing to build, not just the skill to practice.

BAD (too vague, do not produce output like this):
"Build a project using Docker to learn containerization."

GOOD (concrete, buildable, specific):
"Take an existing REST API (or write a small one) and containerize it with \
a multi-stage Dockerfile, add a docker-compose.yml that also runs its \
database, and write a short README documenting how to run it locally with \
one command."

For soft_skills gaps, propose a concrete, completable activity that \
produces visible evidence, not a call to "improve" or "practice" the skill \
in the abstract.

BAD: "Work on your communication skills by talking to people more."

GOOD: "Write a 1000-word technical blog post explaining a project you built \
to a non-technical audience, and publish it publicly (e.g. on a personal \
blog or Dev.to)."

For every roadmap item, provide:
- skill: copied exactly from the corresponding skills_to_cover entry
- category: copied exactly from the corresponding skills_to_cover entry
- priority: copied exactly from the corresponding skills_to_cover entry
- project_title: a short, specific title
- project_description: 2-4 sentences describing exactly what to build or \
do, concrete enough that the student could start today without further \
research into what to build
- proof_of_skill: one sentence, written like a resume bullet point, stating \
what completing this project demonstrates
- estimated_time: a rough, human-friendly estimate (e.g. "a weekend", \
"1-2 weeks")
- difficulty: "beginner", "intermediate", or "advanced\""""


CATEGORIES = ("technical_skills", "tools_and_frameworks", "soft_skills")


def _skills_to_cover(gap_analysis: GapAnalysis) -> list[dict]:
    skills_to_cover = []
    for category in CATEGORIES:
        gap = getattr(gap_analysis, category)
        for skill in gap.missing_required:
            skills_to_cover.append(
                {"skill": skill, "category": category, "priority": "required"}
            )
        for skill in gap.missing_preferred:
            skills_to_cover.append(
                {"skill": skill, "category": category, "priority": "preferred"}
            )
    return skills_to_cover


def build_roadmap(gap_analysis: GapAnalysis) -> Roadmap:
    skills_to_cover = _skills_to_cover(gap_analysis)
    if not skills_to_cover:
        return Roadmap(projects=[])

    llm = get_llm(temperature=0.0).with_structured_output(Roadmap)
    payload = json.dumps({"skills_to_cover": skills_to_cover}, indent=2)
    return llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=payload),
        ]
    )
