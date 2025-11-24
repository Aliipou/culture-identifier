"""API routes."""
from fastapi import APIRouter, HTTPException, Request
from loguru import logger
import time

from ..models import AnalyzeRequest, AnalyzeResponse, CulturalMatch, Projection, HealthResponse


router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest, req: Request):
    """Analyze user text and find matching cultural figures.

    Args:
        request: Analysis request with user text
        req: FastAPI request object for accessing app state

    Returns:
        Analysis response with matches and projections
    """
    start_time = time.time()

    try:
        # Get analyzer from app state
        analyzer = req.app.state.analyzer

        # Perform analysis
        matches, projection_data, user_summary = analyzer.analyze(
            text=request.text,
            top_k=request.top_k,
            mode=request.mode
        )

        # Build response
        cultural_matches = [
            CulturalMatch(**match) for match in matches
        ]

        projections = [
            Projection(**proj) for proj in projection_data
        ]

        processing_time = (time.time() - start_time) * 1000  # Convert to ms

        response = AnalyzeResponse(
            matches=cultural_matches,
            projection=projections,
            user_embedding_summary=user_summary,
            processing_time_ms=processing_time
        )

        logger.info(f"Analysis completed in {processing_time:.2f}ms")
        return response

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/health", response_model=HealthResponse)
async def health_check(req: Request):
    """Check API health status.

    Args:
        req: FastAPI request object for accessing app state

    Returns:
        Health status response
    """
    try:
        vector_store = req.app.state.vector_store
        return HealthResponse(
            status="healthy",
            model_loaded=True,
            index_size=vector_store.size()
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            model_loaded=False,
            index_size=0
        )
