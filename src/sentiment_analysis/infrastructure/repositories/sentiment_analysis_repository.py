"""Implementation of the sentiment analysis repository."""
from datetime import datetime
from typing import List, Optional

from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis
from sentiment_analysis.domain.repositories.sentiment_analysis_repository import SentimentAnalysisRepository as SentimentAnalysisRepositoryInterface


class SentimentAnalysisRepository(SentimentAnalysisRepositoryInterface):
    """Implementation of the sentiment analysis repository."""

    def __init__(self):
        """Initialize the repository."""
        self._analyses: List[SentimentAnalysis] = []

    async def create(self, sentiment_analysis: SentimentAnalysis) -> SentimentAnalysis:
        """Create a new sentiment analysis.
        
        Args:
            sentiment_analysis: SentimentAnalysis entity to create
            
        Returns:
            Created SentimentAnalysis entity
        """
        self._analyses.append(sentiment_analysis)
        return sentiment_analysis

    async def get_by_comment_id(self, comment_id: int) -> Optional[SentimentAnalysis]:
        """Get sentiment analysis by comment ID.
        
        Args:
            comment_id: ID of the comment
            
        Returns:
            SentimentAnalysis entity if found, None otherwise
        """
        for analysis in self._analyses:
            if analysis.comment_id == comment_id:
                return analysis
        return None

    async def get_by_subfeddit_id(
        self,
        subfeddit_id: int,
        limit: int = 25,
        skip: int = 0
    ) -> List[SentimentAnalysis]:
        """Get sentiment analyses by subfeddit ID.
        
        Args:
            subfeddit_id: ID of the subfeddit
            limit: Maximum number of analyses to return
            skip: Number of analyses to skip
            
        Returns:
            List of SentimentAnalysis entities
        """
        filtered = [
            analysis for analysis in self._analyses
            if analysis.subfeddit_id == subfeddit_id
        ]
        return sorted(filtered, key=lambda x: x.created_at, reverse=True)[skip:skip + limit]

    async def save(self, analysis: SentimentAnalysis) -> None:
        """Save a sentiment analysis result.
        
        Args:
            analysis: The sentiment analysis result to save
        """
        if not analysis.comment_text:
            raise ValueError("Comment text is required for sentiment analysis")
        self._analyses.append(analysis)

    async def get_by_subfeddit(
        self,
        subfeddit_id: int,
        limit: int = 25,
        start_time: datetime | None = None,
        end_time: datetime | None = None
    ) -> List[SentimentAnalysis]:
        """Get sentiment analyses for a subfeddit.
        
        Args:
            subfeddit_id: ID of the subfeddit
            limit: Maximum number of analyses to return
            start_time: Optional start time for filtering
            end_time: Optional end time for filtering
            
        Returns:
            List of sentiment analyses
        """
        filtered = [
            analysis for analysis in self._analyses
            if analysis.subfeddit_id == subfeddit_id
            and (not start_time or analysis.created_at >= start_time)
            and (not end_time or analysis.created_at <= end_time)
        ]
        return sorted(filtered, key=lambda x: x.created_at, reverse=True)[:limit]
