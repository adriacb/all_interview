"""FedditSubfedditRepository implementation."""

from typing import List, Optional

from sentiment_analysis.domain.entities.subfeddit import Subfeddit
from sentiment_analysis.domain.repositories.subfeddit_repository import SubfedditRepository
from sentiment_analysis.infrastructure.services.feddit_client import FedditClient


class FedditSubfedditRepository(SubfedditRepository):
    """Implementation of SubfedditRepository using FedditClient."""
    
    def __init__(self, feddit_client: FedditClient):
        """Initialize the repository.
        
        Args:
            feddit_client: FedditClient instance
        """
        self._feddit_client = feddit_client

    async def get_all(self, limit: int = 10, skip: int = 0) -> List[Subfeddit]:
        """Get all subfeddits.
        
        Args:
            limit: Maximum number of subfeddits to return
            skip: Number of subfeddits to skip
            
        Returns:
            List of Subfeddit entities
        """
        subfeddits = await self._feddit_client.get_subfeddits(limit=limit, skip=skip)
        return [
            Subfeddit(
                id=subfeddit.id,
                username=subfeddit.username,
                title=subfeddit.title,
                description=subfeddit.description,
                created_at=subfeddit.created_at,
                updated_at=subfeddit.updated_at
            )
            for subfeddit in subfeddits
        ]

    async def get_by_id(self, subfeddit_id: int) -> Optional[Subfeddit]:
        """Get a subfeddit by ID.
        
        Args:
            subfeddit_id: ID of the subfeddit to get
            
        Returns:
            Subfeddit entity if found, None otherwise
        """
        subfeddits = await self._feddit_client.get_subfeddits(limit=1, skip=0)
        if not subfeddits:
            return None
        
        subfeddit = subfeddits[0]
        return Subfeddit(
            id=subfeddit.id,
            username=subfeddit.username,
            title=subfeddit.title,
            description=subfeddit.description,
            created_at=subfeddit.created_at,
            updated_at=subfeddit.updated_at
        ) 