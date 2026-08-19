import json

from app.graph.build_graph import compiled_graph
from scripts.test_gap_analyzer import SAMPLE_RESUME_WITH_GAPS
from scripts.test_jd_parser import SAMPLE_JD

SAMPLE_RESUME_UNRELATED = """
John Smith
Administrative Assistant

Skills: Excel, PowerPoint, basic HTML, typing 70 WPM

Experience:
Office Administrator, Local Realty Group (2021-2024)
- Maintained spreadsheets in Excel to track property listings
- Created PowerPoint presentations for weekly sales meetings
- Updated the company's static HTML website with new listing pages
- Answered phones and scheduled appointments for agents

Education:
A.A. Business Administration, Community College (2019-2021)
"""


def run_case(label: str, job_description: str, resume_text: str) -> None:
    result = compiled_graph.invoke(
        {"job_description": job_description, "resume_text": resume_text}
    )
    print(f"--- {label} ---")
    print(
        json.dumps(
            {
                "gap_analysis": result["gap_analysis"].model_dump(),
                "roadmap": result["roadmap"].model_dump(),
            },
            indent=2,
        )
    )


def main() -> None:
    run_case("resume with real gaps", SAMPLE_JD, SAMPLE_RESUME_WITH_GAPS)
    run_case("resume almost entirely unrelated", SAMPLE_JD, SAMPLE_RESUME_UNRELATED)


if __name__ == "__main__":
    main()
