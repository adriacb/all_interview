"""API routes for the sentiment analysis microservice."""

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sentiment_analysis.application.services.sentiment_service import SentimentService
from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis
from sentiment_analysis.api.dependencies import get_sentiment_service
from sentiment_analysis.logger import configure_logger

router = APIRouter(prefix="/api/v1/sentiment")
logger = configure_logger().bind(service="api")


@router.get("/{subfeddit}", response_model=List[SentimentAnalysis])
async def analyze_subfeddit_sentiment(
    subfeddit: str,
    limit: int = 25,
    sentiment_service: SentimentService = Depends(get_sentiment_service)
) -> List[SentimentAnalysis]:
    """Analyze sentiment of comments in a subfeddit.
    
    Args:
        subfeddit: Name of the subfeddit to analyze
        limit: Maximum number of comments to analyze (default: 25)
        sentiment_service: Injected sentiment service
        
    Returns:
        List of sentiment analysis results
        
    Raises:
        HTTPException: If an error occurs during analysis
    """
    try:
        logger.info(
            "Analyzing subfeddit sentiment",
            subfeddit=subfeddit,
            limit=limit
        )
        
        analyses = await sentiment_service.analyze_subfeddit_sentiment(
            subfeddit=subfeddit,
            limit=limit
        )
        
        logger.info(
            "Successfully analyzed subfeddit sentiment",
            subfeddit=subfeddit,
            analysis_count=len(analyses)
        )
        
        return analyses
    except Exception as e:
        logger.error(
            "Failed to analyze subfeddit sentiment",
            subfeddit=subfeddit,
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze sentiment: {str(e)}"
        ) 