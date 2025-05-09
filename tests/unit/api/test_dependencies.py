"""Tests for dependency injection functions."""

import pytest
from unittest.mock import Mock
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

from sentiment_analysis.api.dependencies import (
    get_feddit_client,
    get_sentiment_analyzer,
    get_sentiment_analysis_repository,
    get_sentiment_service
)
from sentiment_analysis.infrastructure.clients.feddit_client import FedditClient
from sentiment_analysis.infrastructure.sentiment_analyzer import SentimentAnalyzer
from sentiment_analysis.domain.repositories.sentiment_analysis_repository import SentimentAnalysisRepository
from sentiment_analysis.application.services.sentiment_service import SentimentService


def test_get_feddit_client():
    """Test that get_feddit_client returns a FedditClient instance."""
    client = get_feddit_client()
    assert isinstance(client, FedditClient)


def test_get_sentiment_analyzer():
    """Test that get_sentiment_analyzer returns a SentimentAnalyzer instance."""
    analyzer = get_sentiment_analyzer()
    assert isinstance(analyzer, SentimentAnalyzer)


def test_get_sentiment_analysis_repository():
    """Test that get_sentiment_analysis_repository returns a SentimentAnalysisRepository instance."""
    repository = get_sentiment_analysis_repository()
    assert isinstance(repository, SentimentAnalysisRepository)


def test_get_sentiment_service():
    """Test that get_sentiment_service returns a SentimentService with all dependencies."""
    # Create mock dependencies
    mock_client = Mock(spec=FedditClient)
    mock_analyzer = Mock(spec=SentimentAnalyzer)
    mock_repository = Mock(spec=SentimentAnalysisRepository)
    
    # Call get_sentiment_service directly with our mock dependencies
    service = get_sentiment_service(
        feddit_client=mock_client,
        sentiment_analyzer=mock_analyzer,
        sentiment_analysis_repository=mock_repository
    )
    
    # Verify it's a SentimentService
    assert isinstance(service, SentimentService)
    
    # Verify dependencies were injected correctly
    assert service.feddit_client == mock_client
    assert service.sentiment_analyzer == mock_analyzer
    assert service.sentiment_analysis_repository == mock_repository


def test_get_sentiment_service_with_fastapi():
    """Test that get_sentiment_service works with FastAPI's dependency injection."""
    # Create a test FastAPI app
    app = FastAPI()
    
    # Create mock dependencies
    mock_client = Mock(spec=FedditClient)
    mock_analyzer = Mock(spec=SentimentAnalyzer)
    mock_repository = Mock(spec=SentimentAnalysisRepository)
    
    # Override the dependency providers
    app.dependency_overrides[get_feddit_client] = lambda: mock_client
    app.dependency_overrides[get_sentiment_analyzer] = lambda: mock_analyzer
    app.dependency_overrides[get_sentiment_analysis_repository] = lambda: mock_repository
    
    # Add a test endpoint that uses get_sentiment_service
    @app.get("/test")
    def test_endpoint(service: SentimentService = Depends(get_sentiment_service)):
        assert isinstance(service, SentimentService)
        assert service.feddit_client == mock_client
        assert service.sentiment_analyzer == mock_analyzer
        assert service.sentiment_analysis_repository == mock_repository
        return {"status": "ok"}
    
    # Create a test client
    client = TestClient(app)
    
    # Make a request to test the dependency injection
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_sentiment_service_dependency_validation():
    """Test that get_sentiment_service validates its dependencies."""
    # Create mock dependencies
    mock_client = Mock(spec=FedditClient)
    mock_analyzer = Mock(spec=SentimentAnalyzer)
    mock_repository = Mock(spec=SentimentAnalysisRepository)
    
    # Test with None dependencies
    with pytest.raises(ValueError, match="FedditClient is required"):
        get_sentiment_service(None, mock_analyzer, mock_repository)
    
    with pytest.raises(ValueError, match="SentimentAnalyzer is required"):
        get_sentiment_service(mock_client, None, mock_repository)
    
    with pytest.raises(ValueError, match="SentimentAnalysisRepository is required"):
        get_sentiment_service(mock_client, mock_analyzer, None)
