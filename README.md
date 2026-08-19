# SkillBridge — Backend

A FastAPI backend that identifies the skill gap between a job description
and a candidate's resume, then suggests concrete, buildable projects to
close that gap.

Given a job description and a resume, the system:
1. Extracts required skills from the JD
2. Extracts current skills from the resume
3. Diffs the two into a gap analysis (matched / missing-required /
   missing-preferred, per category)
4. Turns each missing skill into a specific project suggestion — not a
   course, not generic advice

## Tech stack
- FastAPI
- LangGraph (agent orchestration)
- Gemini (via `langchain-google-genai`), structured output via native
  JSON-schema decoding
- No database — this MVP is fully stateless

## Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.1-flash-lite
```

## Running the server

```powershell
uvicorn app.main:app --reload
```

- `GET /health` → `{"status": "ok"}`
- `POST /analyze` — see below

## API

### `POST /analyze`

Request:
```json
{
  "job_description": "...",
  "resume_text": "..."
}
```
Both fields are required, non-empty strings.

Response:
```json
{
  "gap_analysis": {
    "technical_skills": { "matched": [...], "missing_required": [...], "missing_preferred": [...] },
    "tools_and_frameworks": { "matched": [...], "missing_required": [...], "missing_preferred": [...] },
    "soft_skills": { "matched": [...], "missing_required": [...], "missing_preferred": [...] }
  },
  "roadmap": {
    "projects": [
      {
        "skill": "...",
        "category": "...",
        "priority": "required | preferred",
        "project_title": "...",
        "project_description": "...",
        "proof_of_skill": "...",
        "estimated_time": "...",
        "difficulty": "beginner | intermediate | advanced"
      }
    ]
  }
}
```

Errors: invalid/empty input → `422` with Pydantic validation details.
Any failure during analysis (LLM/API error) → `500` with a generic
message; the real error is logged server-side, not returned to the client.

## Project structure

```
app/
  core/       Settings + shared Gemini client factory
  schemas/    All Pydantic models (requests, responses, agent I/O)
  agents/     One module per agent: jd_parser, resume_parser, gap_analyzer, roadmap
  graph/      LangGraph StateGraph wiring the four agents together
  api/        POST /analyze route
  main.py     FastAPI app entrypoint
scripts/      Standalone scripts to test each agent (and the full graph)
              independently, without needing the server running
```

## Testing individual pieces

Each agent can be exercised on its own, without starting the server:

```powershell
python -m scripts.test_jd_parser
python -m scripts.test_resume_parser
python -m scripts.test_gap_analyzer
python -m scripts.test_gap_analyzer_determinism
python -m scripts.test_roadmap
python -m scripts.test_graph
```
