"""Tests for FedditClient."""

import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime
from httpx import Response, RequestError

from sentiment_analysis.infrastructure.clients.feddit_client import FedditClient
from sentiment_analysis.domain.entities.comment import Comment
from sentiment_analysis.domain.entities.subfeddit import Subfeddit


class TestFedditClient:
    """Test cases for FedditClient."""

    @pytest.fixture
    def client(self):
        """Create a FedditClient instance."""
        return FedditClient(base_url="http://test.com")

    @pytest.mark.asyncio
    async def test_get_subfeddits_success(self, client):
        """Test successful subfeddits fetch."""
        # Mock response data
        mock_data = {
            "subfeddits": [
                {
                    "id": 1,
                    "username": "test_user",
                    "title": "Test Title",
                    "description": "Test Description"
                }
            ]
        }

        # Mock the HTTP client
        mock_response = Response(
            status_code=200,
            request=AsyncMock()
        )
        mock_response.json = lambda: mock_data  # Changed from AsyncMock to regular lambda
        client.client.get = AsyncMock(return_value=mock_response)

        # Call the method
        subfeddits = await client.get_subfeddits(limit=10, skip=0)

        # Verify results
        assert len(subfeddits) == 1
        assert isinstance(subfeddits[0], Subfeddit)
        assert subfeddits[0].id == 1
        assert subfeddits[0].username == "test_user"
        assert subfeddits[0].title == "Test Title"
        assert subfeddits[0].description == "Test Description"

        # Verify API call
        client.client.get.assert_called_once_with(
            "/api/v1/subfeddits/",
            params={"limit": 10, "skip": 0}
        )

    @pytest.mark.asyncio
    async def test_get_comments_success(self, client):
        """Test successful comments fetch."""
        # Mock response data
        mock_data = {
            "comments": [
                {
                    "id": 1,
                    "subfeddit_id": 2,
                    "username": "test_user",
                    "text": "Test comment",
                    "created_at": 1609459200
                }
            ]
        }

        # Mock the HTTP client
        mock_response = Response(
            status_code=200,
            request=AsyncMock()
        )
        mock_response.json = lambda: mock_data  # Changed from AsyncMock to regular lambda
        client.client.get = AsyncMock(return_value=mock_response)

        # Call the method
        comments = await client.get_comments(subfeddit_id=2, limit=25, skip=0)

        # Verify results
        assert len(comments) == 1
        assert isinstance(comments[0], Comment)
        assert comments[0].id == 1
        assert comments[0].subfeddit_id == 2
        assert comments[0].username == "test_user"
        assert comments[0].text == "Test comment"
        assert comments[0].created_at == datetime.fromtimestamp(1609459200)

        # Verify API call
        client.client.get.assert_called_once_with(
            "/api/v1/comments/",
            params={
                "subfeddit_id": 2,
                "limit": 25,
                "skip": 0
            }
        )

    @pytest.mark.asyncio
    async def test_get_subfeddits_error(self, client):
        """Test error handling in subfeddits fetch."""
        # Mock the HTTP client to raise an error
        client.client.get = AsyncMock(side_effect=RequestError("Test error"))

        # Call the method and expect an exception
        with pytest.raises(RequestError):
            await client.get_subfeddits()

        # Verify API call
        client.client.get.assert_called_once_with(
            "/api/v1/subfeddits/",
            params={"limit": 10, "skip": 0}
        )

    @pytest.mark.asyncio
    async def test_get_comments_error(self, client):
        """Test error handling in comments fetch."""
        # Mock the HTTP client to raise an error
        client.client.get = AsyncMock(side_effect=RequestError("Test error"))

        # Call the method and expect an exception
        with pytest.raises(RequestError):
            await client.get_comments(subfeddit_id=1)

        # Verify API call
        client.client.get.assert_called_once_with(
            "/api/v1/comments/",
            params={
                "subfeddit_id": 1,
                "limit": 25,
                "skip": 0
            }
        )

    @pytest.mark.asyncio
    async def test_client_initialization(self):
        """Test client initialization with custom base URL."""
        custom_url = "http://custom.com"
        client = FedditClient(base_url=custom_url)
        assert client.base_url == custom_url
        assert client.client.base_url == custom_url

    @pytest.mark.asyncio
    async def test_client_close(self, client):
        """Test client close method."""
        client.client.aclose = AsyncMock()
        await client.close()
        client.client.aclose.assert_called_once() 