"""Repository interface for sentiment analysis."""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis


class SentimentAnalysisRepository(ABC):
    """Repository interface for sentiment analysis operations."""

    @abstractmethod
    async def create(self, sentiment_analysis: SentimentAnalysis) -> SentimentAnalysis:
        """Create a new sentiment analysis.
        
        Args:
            sentiment_analysis: SentimentAnalysis entity to create
            
        Returns:
            Created SentimentAnalysis entity
        """
        pass

    @abstractmethod
    async def get_by_comment_id(self, comment_id: int) -> Optional[SentimentAnalysis]:
        """Get sentiment analysis by comment ID.
        
        Args:
            comment_id: ID of the comment
            
        Returns:
            SentimentAnalysis entity if found, None otherwise
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    async def save(self, analysis: SentimentAnalysis) -> None:
        """Save a sentiment analysis result.
        
        Args:
            analysis: The sentiment analysis result to save
        """
        pass

    @abstractmethod
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
        pass
