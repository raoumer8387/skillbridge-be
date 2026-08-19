import json

from app.agents.jd_parser import parse_jd

SAMPLE_JD = """
We are looking for a Backend Engineer to join our platform team.

Required:
- 3+ years of experience with Python and building REST APIs
- Strong understanding of relational databases (PostgreSQL preferred)
- Experience with Docker and containerized deployments
- Solid grasp of data structures and algorithms
- Excellent written and verbal communication skills

Nice to have:
- Experience with Kubernetes
- Familiarity with AWS
- Exposure to event-driven architectures
- Comfortable mentoring junior engineers
"""


def main() -> None:
    result = parse_jd(SAMPLE_JD)
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    main()
