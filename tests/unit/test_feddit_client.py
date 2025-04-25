"""Unit tests for the Feddit client service."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from sentiment_analysis.services.feddit_client import FedditClient
from sentiment_analysis.models.subfeddit import Subfeddit
from sentiment_analysis.models.comment import Comment


@pytest.mark.asyncio
async def test_get_subfeddits_success():
    """Test successful fetching of subfeddits."""
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.json = AsyncMock(return_value={
        "subfeddits": [
            {
                "id": 1,
                "username": "test_user",
                "title": "Test Title",
                "description": "Test Description"
            },
            {
                "id": 2,
                "username": "another_user",
                "title": "Another Title",
                "description": "Another Description"
            }
        ]
    })
    mock_response.raise_for_status = AsyncMock()
    mock_client.get.return_value = mock_response

    with patch("httpx.AsyncClient", return_value=mock_client):
        client = FedditClient()
        subfeddits = await client.get_subfeddits(limit=10, skip=0)
        
        assert len(subfeddits) == 2
        assert isinstance(subfeddits[0], Subfeddit)
        assert subfeddits[0].id == 1
        assert subfeddits[0].username == "test_user"
        assert subfeddits[0].title == "Test Title"
        assert subfeddits[0].description == "Test Description"
        
        mock_client.get.assert_called_once_with(
            "/api/v1/subfeddits/",
            params={"limit": 10, "skip": 0}
        )


@pytest.mark.asyncio
async def test_get_comments_success():
    """Test successful fetching of comments."""
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.json = AsyncMock(return_value={
        "comments": [
            {
                "id": 1,
                "username": "test_user",
                "text": "Test comment",
                "created_at": 1234567890
            },
            {
                "id": 2,
                "username": "another_user",
                "text": "Another comment",
                "created_at": 1234567891
            }
        ]
    })
    mock_response.raise_for_status = AsyncMock()
    mock_client.get.return_value = mock_response

    with patch("httpx.AsyncClient", return_value=mock_client):
        client = FedditClient()
        comments = await client.get_comments(subfeddit_id=1, limit=25, skip=0)
        
        assert len(comments) == 2
        assert isinstance(comments[0], Comment)
        assert comments[0].id == 1
        assert comments[0].username == "test_user"
        assert comments[0].text == "Test comment"
        assert comments[0].created_at == 1234567890
        
        mock_client.get.assert_called_once_with(
            "/api/v1/comments/",
            params={"subfeddit_id": 1, "limit": 25, "skip": 0}
        )


@pytest.mark.asyncio
async def test_get_subfeddits_error():
    """Test error handling when fetching subfeddits."""
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.status_code = 404
    mock_response.json = AsyncMock(side_effect=httpx.HTTPError("Not Found"))
    mock_response.raise_for_status = AsyncMock(side_effect=httpx.HTTPError("Not Found"))
    mock_client.get.return_value = mock_response

    with patch("httpx.AsyncClient", return_value=mock_client):
        client = FedditClient()
        with pytest.raises(httpx.HTTPError) as exc_info:
            await client.get_subfeddits()
        
        assert str(exc_info.value) == "Not Found"
        mock_client.get.assert_called_once_with(
            "/api/v1/subfeddits/",
            params={"limit": 10, "skip": 0}
        )


@pytest.mark.asyncio
async def test_get_comments_error():
    """Test error handling when fetching comments."""
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.status_code = 404
    mock_response.json = AsyncMock(side_effect=httpx.HTTPError("Not Found"))
    mock_response.raise_for_status = AsyncMock(side_effect=httpx.HTTPError("Not Found"))
    mock_client.get.return_value = mock_response

    with patch("httpx.AsyncClient", return_value=mock_client):
        client = FedditClient()
        with pytest.raises(httpx.HTTPError) as exc_info:
            await client.get_comments(subfeddit_id=1)
        
        assert str(exc_info.value) == "Not Found"
        mock_client.get.assert_called_once_with(
            "/api/v1/comments/",
            params={"subfeddit_id": 1, "limit": 25, "skip": 0}
        )


@pytest.mark.asyncio
async def test_client_initialization():
    """Test client initialization with custom base URL."""
    custom_base_url = "http://custom.api:8080"
    with patch("httpx.AsyncClient") as mock_client_class:
        client = FedditClient(base_url=custom_base_url)
        mock_client_class.assert_called_once_with(base_url=custom_base_url)


@pytest.mark.asyncio
async def test_client_close():
    """Test client cleanup on close."""
    mock_client = AsyncMock()
    with patch("httpx.AsyncClient", return_value=mock_client):
        client = FedditClient()
        await client.close()
        mock_client.aclose.assert_called_once() 