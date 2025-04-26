"""Comment repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from sentiment_analysis.domain.entities.comment import Comment


class CommentRepository(ABC):
    """Interface for Comment repository."""
    
    @abstractmethod
    async def get_by_subfeddit(
        self,
        subfeddit_id: int,
        limit: int = 25,
        skip: int = 0
    ) -> List[Comment]:
        """Get comments by subfeddit ID.
        
        Args:
            subfeddit_id: ID of the subfeddit
            limit: Maximum number of comments to return
            skip: Number of comments to skip
            
        Returns:
            List of Comment entities
        """
        pass

    @abstractmethod
    async def get_by_id(self, comment_id: int) -> Optional[Comment]:
        """Get a comment by ID.
        
        Args:
            comment_id: ID of the comment to get
            
        Returns:
            Comment entity if found, None otherwise
        """
        pass
