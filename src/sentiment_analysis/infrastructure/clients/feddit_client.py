"""Client for interacting with the Feddit API."""

from typing import List, Optional
import httpx
from datetime import datetime

from sentiment_analysis.logger import configure_logger
from sentiment_analysis.domain.entities.comment import Comment
from sentiment_analysis.domain.entities.subfeddit import Subfeddit


class FedditClient:
    """Client for interacting with the Feddit API.

    This client provides methods to fetch subfeddits and comments from the Feddit API.
    """

    def __init__(self, base_url: str = "http://0.0.0.0:8080"):
        """Initialize the Feddit client.

        Args:
            base_url: Base URL of the Feddit API. Defaults to "http://0.0.0.0:8080".
        """
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)
        self.logger = configure_logger().bind(service="feddit_client")

    async def get_subfeddits(
        self, limit: int = 10, skip: int = 0
    ) -> List[Subfeddit]:
        """Get a list of subfeddits.

        Args:
            limit: Maximum number of subfeddits to return. Defaults to 10.
            skip: Number of subfeddits to skip. Defaults to 0.

        Returns:
            List of Subfeddit objects.

        Raises:
            httpx.HTTPError: If the API request fails.
        """
        self.logger.info(
            "Fetching subfeddits",
            limit=limit,
            skip=skip
        )
        try:
            response = await self.client.get(
                "/api/v1/subfeddits/",
                params={"limit": limit, "skip": skip}
            )
            response.raise_for_status()
            data = await response.json()
            
            # Convert API response to domain entities
            subfeddits = []
            for subfeddit_data in data["subfeddits"]:
                # Convert timestamps to datetime objects
                created_at = datetime.fromtimestamp(subfeddit_data["created_at"])
                updated_at = datetime.fromtimestamp(subfeddit_data["updated_at"])
                
                subfeddit = Subfeddit(
                    id=subfeddit_data["id"],
                    username=subfeddit_data["username"],
                    title=subfeddit_data["title"],
                    description=subfeddit_data["description"],
                    created_at=created_at,
                    updated_at=updated_at
                )
                subfeddits.append(subfeddit)
            
            self.logger.info(
                "Successfully fetched subfeddits",
                count=len(subfeddits)
            )
            return subfeddits
        except httpx.HTTPError as e:
            self.logger.error(
                "Failed to fetch subfeddits",
                error=str(e),
                status_code=e.response.status_code if hasattr(e, 'response') else None
            )
            raise

    async def get_comments(
        self,
        subfeddit_id: int,
        limit: int = 25,
        skip: int = 0
    ) -> List[Comment]:
        """Get comments for a specific subfeddit.

        Args:
            subfeddit_id: ID of the subfeddit.
            limit: Maximum number of comments to return. Defaults to 25.
            skip: Number of comments to skip. Defaults to 0.

        Returns:
            List of Comment objects.

        Raises:
            httpx.HTTPError: If the API request fails.
        """
        self.logger.info(
            "Fetching comments",
            subfeddit_id=subfeddit_id,
            limit=limit,
            skip=skip
        )
        try:
            response = await self.client.get(
                "/api/v1/comments/",
                params={
                    "subfeddit_id": subfeddit_id,
                    "limit": limit,
                    "skip": skip
                }
            )
            response.raise_for_status()
            data = await response.json()
            
            # Convert API response to domain entities
            comments = []
            for comment_data in data["comments"]:
                # Convert timestamps to datetime objects
                created_at = datetime.fromtimestamp(comment_data["created_at"])
                updated_at = datetime.fromtimestamp(comment_data["updated_at"])
                
                comment = Comment(
                    id=comment_data["id"],
                    subfeddit_id=comment_data["subfeddit_id"],
                    username=comment_data["username"],
                    text=comment_data["text"],
                    created_at=created_at,
                    updated_at=updated_at
                )
                comments.append(comment)
            
            self.logger.info(
                "Successfully fetched comments",
                count=len(comments)
            )
            return comments
        except httpx.HTTPError as e:
            self.logger.error(
                "Failed to fetch comments",
                error=str(e),
                status_code=e.response.status_code if hasattr(e, 'response') else None
            )
            raise

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
        self.logger.info("Feddit client closed") 