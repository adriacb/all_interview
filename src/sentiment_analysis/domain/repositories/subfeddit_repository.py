"""Subfeddit repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from sentiment_analysis.domain.entities.subfeddit import Subfeddit


class SubfedditRepository(ABC):
    """Interface for Subfeddit repository."""
    
    @abstractmethod
    async def get_subfeddits(self, limit: int = 10, skip: int = 0) -> List[Subfeddit]:
        """Get all subfeddits.
        
        Args:
            limit: Maximum number of subfeddits to return
            skip: Number of subfeddits to skip
            
        Returns:
            List of Subfeddit entities
        """
        pass

    @abstractmethod
    async def get_by_id(self, subfeddit_id: int) -> Optional[Subfeddit]:
        """Get a subfeddit by ID.
        
        Args:
            subfeddit_id: ID of the subfeddit to get
            
        Returns:
            Subfeddit entity if found, None otherwise
        """
        pass
