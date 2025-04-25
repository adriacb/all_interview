"""AnalyzeSentiment use case."""

from datetime import datetime

from sentiment_analysis.domain.entities.comment import Comment
from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis, SentimentType
from sentiment_analysis.domain.repositories.sentiment_analysis_repository import SentimentAnalysisRepository


class AnalyzeSentimentUseCase:
    """Use case for analyzing sentiment of comments."""
    
    def __init__(
        self,
        sentiment_analysis_repository: SentimentAnalysisRepository
    ):
        """Initialize the use case.
        
        Args:
            sentiment_analysis_repository: Repository for sentiment analyses
        """
        self._sentiment_analysis_repository = sentiment_analysis_repository

    async def execute(self, comment: Comment) -> SentimentAnalysis:
        """Execute the use case.
        
        Args:
            comment: Comment entity to analyze
            
        Returns:
            SentimentAnalysis entity
        """
        # TODO: Implement actual sentiment analysis logic
        # For now, return a dummy analysis
        sentiment_analysis = SentimentAnalysis(
            id=0,  # Will be set by repository
            comment_id=comment.id,
            sentiment_type=SentimentType.NEUTRAL,
            confidence_score=0.5,
            created_at=datetime.now()
        )
        
        return await self._sentiment_analysis_repository.create(sentiment_analysis) 