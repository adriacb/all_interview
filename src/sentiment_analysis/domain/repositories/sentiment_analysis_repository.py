"""SentimentAnalysis repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis


class SentimentAnalysisRepository(ABC):
    """Interface for SentimentAnalysis repository."""
    
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