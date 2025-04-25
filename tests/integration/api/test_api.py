"""Integration tests for API endpoints."""

import os
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from sentiment_analysis.api.main import app
from sentiment_analysis.domain.entities.comment import Comment
from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis
from sentiment_analysis.domain.entities.subfeddit import Subfeddit
from sentiment_analysis.application.services.sentiment_service import SentimentService


@pytest.fixture(autouse=True)
def mock_openai_api_key():
    """Mock OpenAI API key for all tests."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        yield


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def mock_subfeddit():
    """Create a mock subfeddit."""
    return Subfeddit(
        id=1,
        username="test_user",
        title="test_subfeddit",
        description="A test subfeddit"
    )


@pytest.fixture
def mock_comment():
    """Create a mock comment."""
    timestamp = datetime(2024, 1, 1, 12)
    return Comment(
        id=1,
        subfeddit_id=1,
        username="user1",
        text="Positive comment",
        created_at=timestamp,
        updated_at=timestamp
    )


@pytest.fixture
def mock_analysis():
    """Create a mock sentiment analysis."""
    return SentimentAnalysis(
        id=1,
        comment_id=1,
        subfeddit_id=1,
        sentiment_score=0.5,
        sentiment_label="positive",
        created_at=datetime(2024, 1, 1, 12)
    )


@pytest.fixture
def mock_sentiment_service(mock_subfeddit, mock_comment, mock_analysis):
    """Create a mock sentiment service."""
    service = AsyncMock(spec=SentimentService)
    service.analyze_subfeddit_sentiment = AsyncMock(return_value=[mock_analysis])
    return service


class TestSentimentAnalysisEndpoint:
    """Test cases for the sentiment analysis endpoint."""

    @patch("sentiment_analysis.api.dependencies.get_sentiment_service")
    def test_analyze_subfeddit_sentiment_success(
        self,
        mock_service_factory,
        client,
        mock_sentiment_service,
        mock_analysis
    ):
        """Test successful sentiment analysis."""
        # Setup mocks
        mock_service_factory.return_value = mock_sentiment_service

        # Test request
        response = client.get(
            "/api/v1/sentiment/test_subfeddit",
            params={
                "limit": 10,
                "start_time": "2024-01-01T00:00:00",
                "end_time": "2024-01-02T00:00:00"
            }
        )

        # Assertions
        assert response.status_code == 200
        assert "analyses" in response.json()
        assert len(response.json()["analyses"]) == 1
        assert response.json()["analyses"][0]["sentiment_score"] == 0.5

        # Verify mocks were called
        mock_sentiment_service.analyze_subfeddit_sentiment.assert_called_once_with(
            subfeddit="test_subfeddit",
            limit=10,
            start_time=datetime(2024, 1, 1),
            end_time=datetime(2024, 1, 2)
        )

    @patch("sentiment_analysis.api.dependencies.get_sentiment_service")
    def test_analyze_subfeddit_sentiment_subfeddit_not_found(
        self,
        mock_service_factory,
        client,
        mock_sentiment_service
    ):
        """Test sentiment analysis with non-existent subfeddit."""
        # Setup mocks
        mock_service_factory.return_value = mock_sentiment_service
        mock_sentiment_service.analyze_subfeddit_sentiment.side_effect = ValueError("Subfeddit not found")

        # Test request
        response = client.get(
            "/api/v1/sentiment/non_existent",
            params={
                "limit": 10
            }
        )

        # Assertions
        assert response.status_code == 404
        assert "detail" in response.json()
        assert "Subfeddit not found" in response.json()["detail"]

    @patch("sentiment_analysis.api.dependencies.get_sentiment_service")
    def test_analyze_subfeddit_sentiment_api_error(
        self,
        mock_service_factory,
        client,
        mock_sentiment_service
    ):
        """Test sentiment analysis with API error."""
        # Setup mocks
        mock_service_factory.return_value = mock_sentiment_service
        mock_sentiment_service.analyze_subfeddit_sentiment.side_effect = Exception("API Error")

        # Test request
        response = client.get(
            "/api/v1/sentiment/test_subfeddit",
            params={
                "limit": 10
            }
        )

        # Assertions
        assert response.status_code == 500
        assert "detail" in response.json()
        assert "Error analyzing sentiment" in response.json()["detail"]

    @patch("sentiment_analysis.api.dependencies.get_sentiment_service")
    def test_analyze_subfeddit_sentiment_default_limit(
        self,
        mock_service_factory,
        client,
        mock_sentiment_service,
        mock_analysis
    ):
        """Test sentiment analysis with default limit."""
        # Setup mocks
        mock_service_factory.return_value = mock_sentiment_service

        # Test request
        response = client.get("/api/v1/sentiment/test_subfeddit")

        # Assertions
        assert response.status_code == 200
        assert "analyses" in response.json()
        assert len(response.json()["analyses"]) == 1

        # Verify mocks were called with default limit
        mock_sentiment_service.analyze_subfeddit_sentiment.assert_called_once_with(
            subfeddit="test_subfeddit",
            limit=25,
            start_time=None,
            end_time=None
        )

    @patch("sentiment_analysis.api.dependencies.get_sentiment_service")
    def test_analyze_subfeddit_sentiment_sort_by_score(
        self,
        mock_service_factory,
        client,
        mock_sentiment_service
    ):
        """Test sentiment analysis with sorting by score."""
        # Setup mocks
        mock_service_factory.return_value = mock_sentiment_service

        # Create multiple analyses with different scores
        analyses = [
            SentimentAnalysis(
                id=1,
                comment_id=1,
                subfeddit_id=1,
                sentiment_score=0.3,
                sentiment_label="positive",
                created_at=datetime(2024, 1, 1, 12)
            ),
            SentimentAnalysis(
                id=2,
                comment_id=2,
                subfeddit_id=1,
                sentiment_score=0.8,
                sentiment_label="positive",
                created_at=datetime(2024, 1, 1, 12)
            )
        ]
        mock_sentiment_service.analyze_subfeddit_sentiment.return_value = analyses

        # Test request
        response = client.get(
            "/api/v1/sentiment/test_subfeddit",
            params={"sort_by_score": True}
        )

        # Assertions
        assert response.status_code == 200
        assert "analyses" in response.json()
        assert len(response.json()["analyses"]) == 2
        assert response.json()["analyses"][0]["sentiment_score"] == 0.8
        assert response.json()["analyses"][1]["sentiment_score"] == 0.3 