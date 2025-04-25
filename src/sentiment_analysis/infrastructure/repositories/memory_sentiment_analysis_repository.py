"""MemorySentimentAnalysisRepository implementation."""

from typing import Dict, List, Optional
from datetime import datetime

from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis
from sentiment_analysis.domain.repositories.sentiment_analysis_repository import SentimentAnalysisRepository


class MemorySentimentAnalysisRepository(SentimentAnalysisRepository):
    """In-memory implementation of SentimentAnalysisRepository."""
    
    def __init__(self):
        """Initialize the repository."""
        self._analyses: Dict[int, SentimentAnalysis] = {}
        self._next_id = 1

    async def create(self, sentiment_analysis: SentimentAnalysis) -> SentimentAnalysis:
        """Create a new sentiment analysis.
        
        Args:
            sentiment_analysis: SentimentAnalysis entity to create
            
        Returns:
            Created SentimentAnalysis entity
        """
        analysis = SentimentAnalysis(
            id=self._next_id,
            comment_id=sentiment_analysis.comment_id,
            sentiment_type=sentiment_analysis.sentiment_type,
            confidence_score=sentiment_analysis.confidence_score,
            created_at=datetime.now()
        )
        
        self._analyses[self._next_id] = analysis
        self._next_id += 1
        
        return analysis

    async def get_by_comment_id(self, comment_id: int) -> Optional[SentimentAnalysis]:
        """Get sentiment analysis by comment ID.
        
        Args:
            comment_id: ID of the comment
            
        Returns:
            SentimentAnalysis entity if found, None otherwise
        """
        for analysis in self._analyses.values():
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
        # TODO: Implement this when we have a way to get comment IDs by subfeddit
        return [] 