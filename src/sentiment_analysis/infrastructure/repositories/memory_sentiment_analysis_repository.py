"""In-memory implementation of the sentiment analysis repository."""

from typing import List, Optional
from datetime import datetime

from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis
from sentiment_analysis.infrastructure.repositories.sentiment_analysis_repository import SentimentAnalysisRepository


class MemorySentimentAnalysisRepository(SentimentAnalysisRepository):
    """In-memory implementation of SentimentAnalysisRepository."""

    def __init__(self):
        """Initialize the repository."""
        super().__init__()

    async def create(self, sentiment_analysis: SentimentAnalysis) -> SentimentAnalysis:
        """Create a new sentiment analysis.
        
        Args:
            sentiment_analysis: SentimentAnalysis entity to create
            
        Returns:
            Created SentimentAnalysis entity
        """
        return await super().create(sentiment_analysis)

    async def get_by_comment_id(self, comment_id: int) -> Optional[SentimentAnalysis]:
        """Get sentiment analysis by comment ID.
        
        Args:
            comment_id: ID of the comment
            
        Returns:
            SentimentAnalysis entity if found, None otherwise
        """
        return await super().get_by_comment_id(comment_id)

    async def get_by_subfeddit(
        self,
        subfeddit_id: int,
        limit: int = 25,
        skip: int = 0,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        sort_by_score: bool = False,
        sort_direction: str = "desc"
    ) -> List[SentimentAnalysis]:
        """Get sentiment analyses for a subfeddit with filtering and sorting options.
        
        Args:
            subfeddit_id: ID of the subfeddit
            limit: Maximum number of analyses to return
            skip: Number of analyses to skip (for pagination)
            start_time: Optional start time for filtering
            end_time: Optional end time for filtering
            sort_by_score: Whether to sort by sentiment score instead of created_at
            sort_direction: Sort direction ("asc" or "desc")
            
        Returns:
            List of sentiment analyses
        """
        return await super().get_by_subfeddit(
            subfeddit_id=subfeddit_id,
            limit=limit,
            skip=skip,
            start_time=start_time,
            end_time=end_time,
            sort_by_score=sort_by_score,
            sort_direction=sort_direction
        )

    async def save(self, analysis: SentimentAnalysis) -> None:
        """Save a sentiment analysis result.
        
        Args:
            analysis: The sentiment analysis result to save
        """
        await super().save(analysis)
