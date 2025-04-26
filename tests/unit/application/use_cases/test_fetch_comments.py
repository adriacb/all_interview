"""Tests for FetchCommentsUseCase."""

import pytest
from unittest.mock import AsyncMock
from datetime import datetime

from sentiment_analysis.application.use_cases.fetch_comments import FetchCommentsUseCase
from sentiment_analysis.domain.entities.comment import Comment


class TestFetchCommentsUseCase:
    """Test cases for FetchCommentsUseCase."""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository."""
        return AsyncMock()

    @pytest.fixture
    def use_case(self, mock_repository):
        """Create a use case instance."""
        return FetchCommentsUseCase(comment_repository=mock_repository)

    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_repository):
        """Test successful execution of the use case."""
        # Mock repository response
        mock_comments = [
            Comment(
                id=1,
                subfeddit_id=2,
                username="test_user",
                text="Test comment",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        mock_repository.get_comments.return_value = mock_comments

        # Execute use case
        result = await use_case.execute(subfeddit_id=2, limit=25, skip=0)

        # Verify results
        assert len(result) == 1
        assert isinstance(result[0], Comment)
        assert result[0].id == 1
        assert result[0].subfeddit_id == 2
        assert result[0].username == "test_user"
        assert result[0].text == "Test comment"

        # Verify repository call
        mock_repository.get_comments.assert_called_once_with(
            subfeddit_id=2,
            limit=25,
            skip=0
        )

    @pytest.mark.asyncio
    async def test_execute_error(self, use_case, mock_repository):
        """Test error handling in the use case."""
        # Mock repository to raise an error
        mock_repository.get_comments.side_effect = Exception("Test error")

        # Execute use case and expect an exception
        with pytest.raises(Exception) as exc_info:
            await use_case.execute(subfeddit_id=2)

        assert str(exc_info.value) == "Test error"
        mock_repository.get_comments.assert_called_once()
