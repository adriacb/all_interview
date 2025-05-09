"""Tests for FedditClient."""

import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime

from sentiment_analysis.infrastructure.clients.feddit_client import FedditClient
from sentiment_analysis.domain.entities.comment import Comment


@pytest.fixture
def mock_httpx_client():
    """Create a mock httpx client."""
    client = AsyncMock()
    return client


@pytest.fixture
def feddit_client(mock_httpx_client):
    """Create a FedditClient with mocked httpx client."""
    with patch('httpx.AsyncClient', return_value=mock_httpx_client):
        client = FedditClient(base_url="http://test.com")
        return client


class TestFedditClient:
    """Test cases for FedditClient."""

    @pytest.mark.asyncio
    async def test_get_comments_invalid_limit(self, feddit_client):
        """Test get_comments with invalid limit values."""
        # Test limit < 1
        with pytest.raises(ValueError, match="Limit must be between 1 and 100"):
            await feddit_client.get_comments(
                subfeddit_id=1,
                limit=0
            )
        
        # Test limit > 100
        with pytest.raises(ValueError, match="Limit must be between 1 and 100"):
            await feddit_client.get_comments(
                subfeddit_id=1,
                limit=101
            )

    @pytest.mark.asyncio
    async def test_get_comments_success(self, feddit_client, mock_httpx_client):
        """Test successful comment retrieval."""
        # Mock response
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.json = lambda: [{
            "id": 1,
            "subfeddit_id": 1,
            "username": "test_user",
            "text": "Test comment",
            "created_at": 1609459200  # 2021-01-01 00:00:00
        }]
        mock_httpx_client.get.return_value = mock_response

        # Call method
        comments = await feddit_client.get_comments(
            subfeddit_id=1,
            limit=25
        )

        # Verify result
        assert len(comments) == 1
        assert isinstance(comments[0], Comment)
        assert comments[0].id == 1
        assert comments[0].subfeddit_id == 1
        assert comments[0].username == "test_user"
        assert comments[0].text == "Test comment"
        assert comments[0].created_at == datetime.fromtimestamp(1609459200)

        # Verify API call
        mock_httpx_client.get.assert_called_once_with(
            "/api/v1/comments/",
            params={
                "subfeddit_id": 1,
                "limit": 25,
                "skip": 0
            }
        )

    @pytest.mark.asyncio
    async def test_get_comments_error(self, feddit_client, mock_httpx_client):
        """Test error handling in get_comments."""
        # Mock error response
        mock_httpx_client.get.side_effect = Exception("API Error")

        # Call method and expect error
        with pytest.raises(Exception) as exc_info:
            await feddit_client.get_comments(
                subfeddit_id=1,
                limit=25
            )
        
        assert str(exc_info.value) == "API Error"
