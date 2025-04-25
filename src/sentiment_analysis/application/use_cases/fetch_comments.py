"""Use case for fetching comments."""

from typing import List
from datetime import datetime

from sentiment_analysis.domain.entities.comment import Comment
from sentiment_analysis.domain.repositories.comment_repository import CommentRepository
from sentiment_analysis.logger import configure_logger


class FetchCommentsUseCase:
    """Use case for fetching comments.

    This use case handles the business logic for fetching comments from the repository.
    """

    def __init__(self, comment_repository: CommentRepository):
        """Initialize the use case.

        Args:
            comment_repository: Repository for fetching comments.
        """
        self.comment_repository = comment_repository
        self.logger = configure_logger().bind(use_case="fetch_comments")

    async def execute(
        self,
        subfeddit_id: int,
        limit: int = 25,
        skip: int = 0
    ) -> List[Comment]:
        """Execute the use case.

        Args:
            subfeddit_id: ID of the subfeddit to fetch comments for.
            limit: Maximum number of comments to return. Defaults to 25.
            skip: Number of comments to skip. Defaults to 0.

        Returns:
            List of Comment objects.

        Raises:
            Exception: If an error occurs while fetching comments.
        """
        self.logger.info(
            "Fetching comments",
            subfeddit_id=subfeddit_id,
            limit=limit,
            skip=skip
        )
        try:
            comments = await self.comment_repository.get_comments(
                subfeddit_id=subfeddit_id,
                limit=limit,
                skip=skip
            )
            self.logger.info(
                "Successfully fetched comments",
                count=len(comments)
            )
            return comments
        except Exception as e:
            self.logger.error(
                "Failed to fetch comments",
                error=str(e)
            )
            raise 