import json

from app.agents.gap_analyzer import analyze_gap
from app.agents.jd_parser import parse_jd
from app.agents.resume_parser import parse_resume
from scripts.test_jd_parser import SAMPLE_JD
from scripts.test_resume_parser import SAMPLE_RESUME

SAMPLE_RESUME_WITH_GAPS = """
Jane Doe
Software Engineer

Skills: Python, JavaScript, Git, SQL

Experience:
Backend Developer, Acme Co (2022-2024)
- Wrote SQL queries against a PostgreSQL database
- Collaborated closely with product managers to scope features
- Presented sprint demos to stakeholders

Projects:
- Personal blog written in Python
- Class group project: built a CLI tool in Python with a teammate,
  coordinated tasks over weekly stand-ups

Education:
B.S. Computer Science, State University (2018-2022)
- Coursework in data structures, algorithms, and operating systems
"""


def run_case(label: str, jd_skills, resume_text: str) -> None:
    resume_skills = parse_resume(resume_text)
    result = analyze_gap(jd_skills, resume_skills)
    print(f"--- {label} ---")
    print(json.dumps(result.model_dump(), indent=2))


def main() -> None:
    jd_skills = parse_jd(SAMPLE_JD)
    run_case("strong-match resume", jd_skills, SAMPLE_RESUME)
    run_case("resume with real gaps", jd_skills, SAMPLE_RESUME_WITH_GAPS)


if __name__ == "__main__":
    main()
