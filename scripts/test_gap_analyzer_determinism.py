import json

from app.agents.gap_analyzer import analyze_gap
from app.agents.jd_parser import parse_jd
from app.agents.resume_parser import parse_resume
from scripts.test_jd_parser import SAMPLE_JD
from scripts.test_resume_parser import SAMPLE_RESUME

RUNS = 5


def main() -> None:
    jd_skills = parse_jd(SAMPLE_JD)
    resume_skills = parse_resume(SAMPLE_RESUME)

    results = []
    for i in range(RUNS):
        result = analyze_gap(jd_skills, resume_skills).model_dump()
        results.append(result)
        print(f"--- run {i + 1} ---")
        print(json.dumps(result, indent=2))

    all_identical = all(r == results[0] for r in results)
    print(f"\nAll {RUNS} runs identical: {all_identical}")


if __name__ == "__main__":
    main()
