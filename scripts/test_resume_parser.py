import json

from app.agents.resume_parser import parse_resume

SAMPLE_RESUME = """
Jane Doe
Software Engineer

Skills: Python, JavaScript, Git, SQL

Experience:
Backend Developer, Acme Co (2022-2024)
- Built and maintained REST APIs in Python using Flask
- Wrote SQL queries against a PostgreSQL database
- Collaborated closely with product managers to scope features
- Presented sprint demos to stakeholders

Projects:
- Personal blog deployed with Docker on a small VPS
- Class group project: built a CLI tool in Python with a teammate,
  coordinated tasks over weekly stand-ups

Education:
B.S. Computer Science, State University (2018-2022)
- Coursework in data structures, algorithms, and operating systems
"""


def main() -> None:
    result = parse_resume(SAMPLE_RESUME)
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    main()
