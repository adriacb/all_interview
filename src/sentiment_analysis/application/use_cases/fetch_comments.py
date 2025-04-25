"""FetchComments use case."""

from typing import List

from sentiment_analysis.domain.entities.comment import Comment
from sentiment_analysis.domain.repositories.comment_repository import CommentRepository


class FetchCommentsUseCase:
    """Use case for fetching comments."""
    
    def __init__(self, comment_repository: CommentRepository):
        """Initialize the use case.
        
        Args:
            comment_repository: Repository for comments
        """
        self._comment_repository = comment_repository

    async def execute(
        self,
        subfeddit_id: int,
        limit: int = 25,
        skip: int = 0
    ) -> List[Comment]:
        """Execute the use case.
        
        Args:
            subfeddit_id: ID of the subfeddit
            limit: Maximum number of comments to return
            skip: Number of comments to skip
            
        Returns:
            List of Comment entities
        """
        return await self._comment_repository.get_by_subfeddit(
            subfeddit_id=subfeddit_id,
            limit=limit,
            skip=skip
        ) 