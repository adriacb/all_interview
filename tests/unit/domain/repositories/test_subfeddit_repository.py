"""Tests for SubfedditRepository interface."""

import pytest
from datetime import datetime
from typing import List, Optional

from sentiment_analysis.domain.entities.subfeddit import Subfeddit
from sentiment_analysis.domain.repositories.subfeddit_repository import SubfedditRepository


class TestSubfedditRepository:
    """Test cases for SubfedditRepository interface."""
    
    @pytest.mark.asyncio
    async def test_get_subfeddits(self):
        """Test get_subfeddits method."""
        # Create a mock repository
        class MockSubfedditRepository(SubfedditRepository):
            async def get_subfeddits(self, limit: int = 10, skip: int = 0) -> List[Subfeddit]:
                now = datetime.now()
                return [
                    Subfeddit(
                        id=1,
                        username="test_user",
                        title="Test Title",
                        description="Test Description",
                        created_at=now,
                        updated_at=now
                    )
                ]
            
            async def get_by_id(self, subfeddit_id: int) -> Optional[Subfeddit]:
                return None
        
        repo = MockSubfedditRepository()
        subfeddits = await repo.get_subfeddits(limit=10, skip=0)
        
        assert len(subfeddits) == 1
        assert isinstance(subfeddits[0], Subfeddit)
        assert subfeddits[0].id == 1
        assert subfeddits[0].username == "test_user"
        assert subfeddits[0].title == "Test Title"
        assert subfeddits[0].description == "Test Description"
    
    @pytest.mark.asyncio
    async def test_get_subfeddits_with_pagination(self):
        """Test get_subfeddits method with pagination."""
        class MockSubfedditRepository(SubfedditRepository):
            async def get_subfeddits(self, limit: int = 10, skip: int = 0) -> List[Subfeddit]:
                now = datetime.now()
                return [
                    Subfeddit(
                        id=i + 1,  # Ensure positive ID
                        username=f"test_user_{i}",
                        title=f"Test Title {i}",
                        description=f"Test Description {i}",
                        created_at=now,
                        updated_at=now
                    ) for i in range(skip, skip + limit)
                ]
            
            async def get_by_id(self, subfeddit_id: int) -> Optional[Subfeddit]:
                return None
        
        repo = MockSubfedditRepository()
        
        # Test first page
        subfeddits = await repo.get_subfeddits(limit=5, skip=0)
        assert len(subfeddits) == 5
        assert subfeddits[0].id == 1
        assert subfeddits[-1].id == 5
        
        # Test second page
        subfeddits = await repo.get_subfeddits(limit=5, skip=5)
        assert len(subfeddits) == 5
        assert subfeddits[0].id == 6
        assert subfeddits[-1].id == 10
