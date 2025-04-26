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
from sentiment_analysis.infrastructure.clients.feddit_client import FedditClient
from sentiment_analysis.infrastructure.sentiment_analyzer import SentimentAnalyzer
from sentiment_analysis.domain.repositories.sentiment_analysis_repository import SentimentAnalysisRepository


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
    subfeddit = Subfeddit(
        id=1,
        username="test_user",
        title="test_subfeddit",
        description="A test subfeddit"
    )
    print(f"Created mock subfeddit: {subfeddit}")  # Debug print
    return subfeddit


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
def mock_feddit_client(mock_subfeddit, mock_comment):
    """Create a mock FedditClient."""
    client = AsyncMock(spec=FedditClient)
    client.get_subfeddits = AsyncMock(return_value=[mock_subfeddit])
    client.get_comments = AsyncMock(return_value=[mock_comment])
    print(f"Mock get_subfeddits will return: {[mock_subfeddit]}")  # Debug print
    return client


@pytest.fixture
def mock_sentiment_analyzer():
    """Create a mock sentiment analyzer."""
    analyzer = AsyncMock(spec=SentimentAnalyzer)
    analyzer.analyze = AsyncMock(return_value=[SentimentAnalysis(
        id=1,
        comment_id=1,
        subfeddit_id=1,
        sentiment_score=0.5,
        sentiment_label="positive",
        created_at=datetime(2024, 1, 1, 12)
    )])
    return analyzer


@pytest.fixture
def mock_sentiment_analysis_repository():
    """Create a mock sentiment analysis repository."""
    repository = AsyncMock(spec=SentimentAnalysisRepository)
    repository.save = AsyncMock()
    return repository


@pytest.fixture
def mock_sentiment_service(
    mock_subfeddit,
    mock_comment,
    mock_analysis,
    mock_feddit_client,
    mock_sentiment_analyzer,
    mock_sentiment_analysis_repository
):
    """Create a mock sentiment service."""
    service = SentimentService(
        feddit_client=mock_feddit_client,
        sentiment_analyzer=mock_sentiment_analyzer,
        sentiment_analysis_repository=mock_sentiment_analysis_repository
    )
    return service


@pytest.fixture(autouse=True)
def mock_dependencies(mock_sentiment_service):
    """Mock all dependencies."""
    # Create a context manager that patches all external dependencies
    patches = [
        patch("sentiment_analysis.api.dependencies.get_sentiment_service", return_value=mock_sentiment_service),
        patch("sentiment_analysis.infrastructure.clients.feddit_client.FedditClient.get_subfeddits"),
        patch("sentiment_analysis.infrastructure.clients.feddit_client.FedditClient.get_comments"),
        patch("sentiment_analysis.infrastructure.sentiment_analyzer.SentimentAnalyzer.analyze")
    ]
    
    # Start all patches
    mocks = [p.start() for p in patches]
    
    # Configure the mocks
    service_mock, get_subfeddits_mock, get_comments_mock, analyze_mock = mocks
    
    # Set up default returns
    get_subfeddits_mock.return_value = [Subfeddit(
        id=1,
        username="test_user",
        title="test_subfeddit",
        description="A test subfeddit"
    )]
    get_comments_mock.return_value = [Comment(
        id=1,
        subfeddit_id=1,
        username="user1",
        text="Positive comment",
        created_at=datetime(2024, 1, 1, 12),
        updated_at=datetime(2024, 1, 1, 12)
    )]
    analyze_mock.return_value = [SentimentAnalysis(
        id=1,
        comment_id=1,
        subfeddit_id=1,
        sentiment_score=0.5,
        sentiment_label="positive",
        created_at=datetime(2024, 1, 1, 12)
    )]
    
    yield {
        'service': service_mock,
        'get_subfeddits': get_subfeddits_mock,
        'get_comments': get_comments_mock,
        'analyze': analyze_mock
    }
    
    # Stop all patches
    for p in patches:
        p.stop()


@pytest.mark.asyncio
async def test_analyze_subfeddit_sentiment_success(
    client,
    mock_dependencies
):
    """Test successful sentiment analysis."""
    response = client.get(
        "/api/v1/sentiment/test_subfeddit",
        params={"limit": 10}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "analyses" in data
    assert len(data["analyses"]) == 1
    assert data["analyses"][0]["sentiment_score"] == 0.5
    assert data["analyses"][0]["sentiment_label"] == "positive"


@pytest.mark.asyncio
async def test_analyze_subfeddit_sentiment_subfeddit_not_found(
    client,
    mock_dependencies
):
    """Test sentiment analysis when subfeddit is not found."""
    mock_dependencies['get_subfeddits'].return_value = []
    
    subfeddit = "nonexistent_subfeddit"
    response = client.get(
        f"/api/v1/sentiment/{subfeddit}",
        params={"limit": 10}
    )
    
    assert response.status_code == 404
    assert f"Subfeddit '{subfeddit}' not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_analyze_subfeddit_sentiment_api_error(
    client,
    mock_dependencies
):
    """Test sentiment analysis when API call fails."""
    mock_dependencies['get_subfeddits'].side_effect = httpx.HTTPError("API Error")
    
    response = client.get(
        "/api/v1/sentiment/test_subfeddit",
        params={"limit": 10}
    )
    
    assert response.status_code == 500
    assert "Error analyzing sentiment" in response.json()["detail"]


@pytest.mark.asyncio
async def test_analyze_subfeddit_sentiment_default_limit(
    client,
    mock_dependencies
):
    """Test sentiment analysis with default limit."""
    response = client.get("/api/v1/sentiment/test_subfeddit")
    
    assert response.status_code == 200
    mock_dependencies['get_subfeddits'].assert_called_once()
    mock_dependencies['get_comments'].assert_called_once()


@pytest.mark.asyncio
async def test_analyze_subfeddit_sentiment_sort_by_score(
    client,
    mock_dependencies
):
    """Test sentiment analysis with sorting by score."""
    # Create multiple analyses with different scores
    mock_dependencies['analyze'].return_value = [
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
    
    response = client.get(
        "/api/v1/sentiment/test_subfeddit",
        params={"sort_by_score": True}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["analyses"]) == 2
    assert data["analyses"][0]["sentiment_score"] == 0.8
    assert data["analyses"][1]["sentiment_score"] == 0.3


@pytest.mark.asyncio
async def test_analyze_subfeddit_sentiment_time_range(
    client,
    mock_dependencies
):
    """Test sentiment analysis with time range filtering."""
    start_time = datetime(2024, 1, 1, 0)
    end_time = datetime(2024, 1, 2, 0)
    
    response = client.get(
        "/api/v1/sentiment/test_subfeddit",
        params={
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }
    )
    
    assert response.status_code == 200
    mock_dependencies['get_subfeddits'].assert_called_once()
    mock_dependencies['get_comments'].assert_called_once()
