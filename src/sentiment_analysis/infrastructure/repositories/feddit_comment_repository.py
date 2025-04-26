"""FedditCommentRepository implementation."""

from typing import List, Optional

from sentiment_analysis.domain.entities.comment import Comment
from sentiment_analysis.domain.repositories.comment_repository import CommentRepository
from sentiment_analysis.infrastructure.clients.feddit_client import FedditClient


class FedditCommentRepository(CommentRepository):
    """Implementation of CommentRepository using FedditClient."""
    
    def __init__(self, feddit_client: FedditClient):
        """Initialize the repository.
        
        Args:
            feddit_client: FedditClient instance
        """
        self._feddit_client = feddit_client

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
        comments = await self._feddit_client.get_comments(
            subfeddit_id=subfeddit_id,
            limit=limit,
            skip=skip
        )
        return [
            Comment(
                id=comment.id,
                subfeddit_id=comment.subfeddit_id,
                username=comment.username,
                text=comment.text,
                created_at=comment.created_at,
                updated_at=comment.updated_at
            )
            for comment in comments
        ]

    async def get_by_id(self, comment_id: int) -> Optional[Comment]:
        """Get a comment by ID.
        
        Args:
            comment_id: ID of the comment to get
            
        Returns:
            Comment entity if found, None otherwise
        """
        # TODO: Implement this when the API supports it
        return None
