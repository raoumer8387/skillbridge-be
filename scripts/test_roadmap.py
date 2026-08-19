import json

from app.agents.gap_analyzer import analyze_gap
from app.agents.jd_parser import parse_jd
from app.agents.resume_parser import parse_resume
from app.agents.roadmap import build_roadmap
from scripts.test_gap_analyzer import SAMPLE_RESUME_WITH_GAPS
from scripts.test_jd_parser import SAMPLE_JD
from scripts.test_resume_parser import SAMPLE_RESUME


def run_case(label: str, jd_skills, resume_text: str) -> None:
    resume_skills = parse_resume(resume_text)
    gaps = analyze_gap(jd_skills, resume_skills)
    roadmap = build_roadmap(gaps)
    print(f"--- {label}: gap analysis (input) ---")
    print(json.dumps(gaps.model_dump(), indent=2))
    print(f"--- {label}: roadmap (output) ---")
    print(json.dumps(roadmap.model_dump(), indent=2))


def main() -> None:
    jd_skills = parse_jd(SAMPLE_JD)
    run_case("strong-match resume", jd_skills, SAMPLE_RESUME)
    run_case("resume with real gaps", jd_skills, SAMPLE_RESUME_WITH_GAPS)


if __name__ == "__main__":
    main()
