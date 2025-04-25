"""FetchSubfeddits use case."""

from typing import List

from sentiment_analysis.domain.entities.subfeddit import Subfeddit
from sentiment_analysis.domain.repositories.subfeddit_repository import SubfedditRepository


class FetchSubfedditsUseCase:
    """Use case for fetching subfeddits."""
    
    def __init__(self, subfeddit_repository: SubfedditRepository):
        """Initialize the use case.
        
        Args:
            subfeddit_repository: Repository for subfeddits
        """
        self._subfeddit_repository = subfeddit_repository

    async def execute(self, limit: int = 10, skip: int = 0) -> List[Subfeddit]:
        """Execute the use case.
        
        Args:
            limit: Maximum number of subfeddits to return
            skip: Number of subfeddits to skip
            
        Returns:
            List of Subfeddit entities
        """
        return await self._subfeddit_repository.get_all(limit=limit, skip=skip) 