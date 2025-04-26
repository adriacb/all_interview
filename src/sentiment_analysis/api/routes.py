"""API routes for the sentiment analysis microservice."""
from fastapi import APIRouter, Depends, HTTPException

from sentiment_analysis.application.services.sentiment_service import SentimentService
from sentiment_analysis.api.dto import SentimentAnalysisResponseDTO, SentimentAnalysisRequestDTO
from sentiment_analysis.api.dependencies import get_sentiment_service
from sentiment_analysis.logger import configure_logger

router = APIRouter(prefix="/api/v1/sentiment")
logger = configure_logger().bind(service="api")


@router.get("/{subfeddit}", response_model=SentimentAnalysisResponseDTO)
async def analyze_subfeddit_sentiment(
    subfeddit: str,
    request: SentimentAnalysisRequestDTO = Depends(),
    sentiment_service: SentimentService = Depends(get_sentiment_service)
) -> SentimentAnalysisResponseDTO:
    """
    Analyze sentiment for comments in a subfeddit.
    
    Args:
        subfeddit: Name of the subfeddit to analyze
        request: Sentiment analysis request parameters
        sentiment_service: Injected sentiment service
        
    Returns:
        List of sentiment analyses for the comments
    """
    try:
        logger.info(
            "Analyzing subfeddit sentiment",
            subfeddit=subfeddit,
            limit=request.limit
        )
        
        analyses = await sentiment_service.analyze_subfeddit_sentiment(
            subfeddit=subfeddit,
            limit=request.limit,
            start_time=request.start_time,
            end_time=request.end_time
        )
        
        if request.sort_by_score:
            analyses.sort(key=lambda x: x.sentiment_score, reverse=True)
            
        logger.info(
            "Successfully analyzed subfeddit sentiment",
            subfeddit=subfeddit,
            analysis_count=len(analyses)
        )
        
        return SentimentAnalysisResponseDTO(analyses=analyses)
    except ValueError as e:
        logger.error(
            "Invalid input",
            subfeddit=subfeddit,
            error=str(e)
        )
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(
            "Failed to analyze subfeddit sentiment",
            subfeddit=subfeddit,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {str(e)}")
    

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "Ok"}
