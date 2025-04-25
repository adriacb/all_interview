"""Tests for FetchSubfedditsUseCase."""

import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime

from sentiment_analysis.application.use_cases.fetch_subfeddits import FetchSubfedditsUseCase
from sentiment_analysis.domain.entities.subfeddit import Subfeddit


class TestFetchSubfedditsUseCase:
    """Test cases for FetchSubfedditsUseCase."""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository."""
        return AsyncMock()

    @pytest.fixture
    def use_case(self, mock_repository):
        """Create a use case instance."""
        return FetchSubfedditsUseCase(subfeddit_repository=mock_repository)

    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_repository):
        """Test successful execution of the use case."""
        # Mock repository response
        mock_subfeddits = [
            Subfeddit(
                id=1,
                username="test_user",
                title="Test Title",
                description="Test Description",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        mock_repository.get_subfeddits.return_value = mock_subfeddits

        # Execute use case
        result = await use_case.execute(limit=10, skip=0)

        # Verify results
        assert len(result) == 1
        assert isinstance(result[0], Subfeddit)
        assert result[0].id == 1
        assert result[0].username == "test_user"
        assert result[0].title == "Test Title"
        assert result[0].description == "Test Description"

        # Verify repository call
        mock_repository.get_subfeddits.assert_called_once_with(
            limit=10,
            skip=0
        )

    @pytest.mark.asyncio
    async def test_execute_error(self, use_case, mock_repository):
        """Test error handling in the use case."""
        # Mock repository to raise an error
        mock_repository.get_subfeddits.side_effect = Exception("Test error")

        # Execute use case and expect an exception
        with pytest.raises(Exception) as exc_info:
            await use_case.execute()

        assert str(exc_info.value) == "Test error"
        mock_repository.get_subfeddits.assert_called_once() 