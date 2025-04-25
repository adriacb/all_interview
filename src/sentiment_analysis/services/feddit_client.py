"""Client for interacting with the Feddit API."""

from typing import List, Optional
import httpx

from sentiment_analysis.logger import configure_logger
from sentiment_analysis.models.comment import Comment
from sentiment_analysis.models.subfeddit import Subfeddit


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
            subfeddits = [Subfeddit(**subfeddit) for subfeddit in data["subfeddits"]]
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
            comments = [Comment(**comment) for comment in data["comments"]]
            self.logger.info(
                "Successfully fetched comments",
                subfeddit_id=subfeddit_id,
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
        self.logger.info("Closing Feddit client")
        await self.client.aclose() 