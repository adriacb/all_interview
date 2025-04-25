"""Feddit API client."""

import httpx
from typing import List

from sentiment_analysis.domain.entities.subfeddit import Subfeddit
from sentiment_analysis.domain.entities.comment import Comment
from sentiment_analysis.logger import configure_logger


class FedditClient:
    """Client for interacting with the Feddit API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the client.
        
        Args:
            base_url: Base URL of the Feddit API
        """
        self._base_url = base_url
        self._client = httpx.AsyncClient(base_url=base_url)
        self._logger = configure_logger().bind(service="feddit_client")

    async def get_subfeddits(self, limit: int = 10, skip: int = 0) -> List[Subfeddit]:
        """Get a list of subfeddits.
        
        Args:
            limit: Maximum number of subfeddits to return
            skip: Number of subfeddits to skip
            
        Returns:
            List of Subfeddit entities
        """
        self._logger.info(
            "Fetching subfeddits",
            limit=limit,
            skip=skip
        )
        
        try:
            response = await self._client.get(
                "/api/v1/subfeddits/",
                params={"limit": limit, "skip": skip}
            )
            response.raise_for_status()
            
            data = response.json()
            subfeddits = [
                Subfeddit(
                    id=subfeddit["id"],
                    username=subfeddit["username"],
                    title=subfeddit["title"],
                    description=subfeddit["description"],
                    created_at=subfeddit["created_at"],
                    updated_at=subfeddit["updated_at"]
                )
                for subfeddit in data["subfeddits"]
            ]
            
            self._logger.info(
                "Successfully fetched subfeddits",
                count=len(subfeddits)
            )
            
            return subfeddits
            
        except httpx.HTTPError as e:
            self._logger.error(
                "Error fetching subfeddits",
                error=str(e),
                limit=limit,
                skip=skip
            )
            raise

    async def get_comments(
        self,
        subfeddit_id: int,
        limit: int = 25,
        skip: int = 0
    ) -> List[Comment]:
        """Get comments for a subfeddit.
        
        Args:
            subfeddit_id: ID of the subfeddit
            limit: Maximum number of comments to return
            skip: Number of comments to skip
            
        Returns:
            List of Comment entities
        """
        self._logger.info(
            "Fetching comments",
            subfeddit_id=subfeddit_id,
            limit=limit,
            skip=skip
        )
        
        try:
            response = await self._client.get(
                "/api/v1/comments/",
                params={
                    "subfeddit_id": subfeddit_id,
                    "limit": limit,
                    "skip": skip
                }
            )
            response.raise_for_status()
            
            data = response.json()
            comments = [
                Comment(
                    id=comment["id"],
                    subfeddit_id=comment["subfeddit_id"],
                    username=comment["username"],
                    text=comment["text"],
                    created_at=comment["created_at"],
                    updated_at=comment["updated_at"]
                )
                for comment in data["comments"]
            ]
            
            self._logger.info(
                "Successfully fetched comments",
                count=len(comments),
                subfeddit_id=subfeddit_id
            )
            
            return comments
            
        except httpx.HTTPError as e:
            self._logger.error(
                "Error fetching comments",
                error=str(e),
                subfeddit_id=subfeddit_id,
                limit=limit,
                skip=skip
            )
            raise

    async def close(self):
        """Close the client."""
        self._logger.info("Closing Feddit client")
        await self._client.aclose() 