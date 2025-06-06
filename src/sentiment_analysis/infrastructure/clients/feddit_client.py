"""Client for interacting with the Feddit API."""
from typing import List, Dict, Any
import httpx
from datetime import datetime

from sentiment_analysis.logger import configure_logger
from sentiment_analysis.domain.entities.comment import Comment
from sentiment_analysis.domain.entities.subfeddit import Subfeddit
from sentiment_analysis.config import FEDDIT_API_URL


class FedditClient:
    """Client for interacting with the Feddit API.

    This client provides methods to fetch subfeddits and comments from the Feddit API.
    """

    def __init__(self, base_url: str = FEDDIT_API_URL):
        """Initialize the Feddit client.

        Args:
            base_url: Base URL of the Feddit API. Defaults to FEDDIT_API_URL from config.
        """
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)
        self.logger = configure_logger().bind(service="feddit_client")

    async def get_subfeddits(self, limit: int = 10, skip: int = 0) -> List[Subfeddit]:
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
                params={
                    "limit": limit,
                    "skip": skip
                }
            )
            self.logger.info("Fetched response get_subfeddits", response=response)
            response.raise_for_status()
            data = response.json()
            self.logger.info("Fetched data get_subfeddits", data=data)
            
            # Convert API response to domain entities
            subfeddits = []
            for subfeddit_data in data["subfeddits"]:  # Access the subfeddits key
                subfeddit = Subfeddit(
                    id=subfeddit_data["id"],
                    username=subfeddit_data["username"],
                    title=subfeddit_data["title"],
                    description=subfeddit_data["description"]
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

    async def get_subfeddit(
        self, subfeddit_id: int, limit: int = 10, skip: int = 0
    ) -> Dict[str, Any]:
        """Get details of a specific subfeddit including its comments.

        Args:
            subfeddit_id: ID of the subfeddit.
            limit: Maximum number of comments to return. Defaults to 10.
            skip: Number of comments to skip. Defaults to 0.

        Returns:
            Dictionary containing subfeddit details and comments.

        Raises:
            httpx.HTTPError: If the API request fails.
        """
        self.logger.info(
            "Fetching subfeddit details",
            subfeddit_id=subfeddit_id,
            limit=limit,
            skip=skip
        )
        try:
            response = await self.client.get(
                "/api/v1/subfeddit/",
                params={
                    "subfeddit_id": subfeddit_id,
                    "limit": limit,
                    "skip": skip
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Convert comments to domain entities
            comments = []
            for comment_data in data["comments"]:
                comment = Comment(
                    id=comment_data["id"],
                    subfeddit_id=subfeddit_id,
                    username=comment_data["username"],
                    text=comment_data["text"],
                    created_at=datetime.fromtimestamp(comment_data["created_at"])
                )
                comments.append(comment)
            
            # Create subfeddit entity
            subfeddit = Subfeddit(
                id=data["id"],
                username=data["username"],
                title=data["title"],
                description=data["description"]
            )
            
            self.logger.info(
                "Successfully fetched subfeddit details",
                subfeddit_id=subfeddit_id,
                comment_count=len(comments)
            )
            
            return {
                "subfeddit": subfeddit,
                "comments": comments
            }
        except httpx.HTTPError as e:
            self.logger.error(
                "Failed to fetch subfeddit details",
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
            ValueError: If limit is less than 1 or greater than 100.
        """
        if not 1 <= limit <= 100:
            raise ValueError("Limit must be between 1 and 100")
            
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
            data = response.json()
            self.logger.debug("Fetched data get_comments", data=data)
            
            # Convert API response to domain entities
            comments = []
            # Check if data is a list or a dictionary with comments key
            comment_data_list = data if isinstance(data, list) else data.get("comments", [])
            
            for comment_data in comment_data_list:
                # Convert Unix timestamp to naive datetime
                created_at = datetime.fromtimestamp(comment_data["created_at"])
                comment = Comment(
                    id=comment_data["id"],
                    subfeddit_id=subfeddit_id,
                    username=comment_data["username"],
                    text=comment_data["text"],
                    created_at=created_at
                )
                comments.append(comment)
            
            self.logger.info(
                "Successfully fetched comments",
                subfeddit_id=subfeddit_id,
                comment_count=len(comments)
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
