import logging

from fastapi import APIRouter, HTTPException

from app.graph.build_graph import compiled_graph
from app.schemas.models import AnalyzeRequest, AnalyzeResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    try:
        result = compiled_graph.invoke(
            {
                "job_description": request.job_description,
                "resume_text": request.resume_text,
            }
        )
    except Exception:
        logger.exception("Analysis pipeline failed")
        raise HTTPException(
            status_code=500, detail="Analysis failed. Please try again."
        )

    return AnalyzeResponse(
        gap_analysis=result["gap_analysis"],
        roadmap=result["roadmap"],
    )
