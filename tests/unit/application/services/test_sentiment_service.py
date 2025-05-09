"""Tests for the SentimentService."""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock

from sentiment_analysis.application.services.sentiment_service import SentimentService
from sentiment_analysis.domain.entities.comment import Comment
from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis
from sentiment_analysis.domain.entities.subfeddit import Subfeddit
from sentiment_analysis.domain.repositories.sentiment_analysis_repository import SentimentAnalysisRepository
from sentiment_analysis.infrastructure.clients.feddit_client import FedditClient
from sentiment_analysis.infrastructure.sentiment_analyzer import SentimentAnalyzer


@pytest.fixture
def mock_feddit_client():
    """Create a mock FedditClient."""
    client = AsyncMock(spec=FedditClient)
    return client


@pytest.fixture
def mock_sentiment_analyzer():
    """Create a mock SentimentAnalyzer."""
    analyzer = AsyncMock(spec=SentimentAnalyzer)
    return analyzer


@pytest.fixture
def mock_repository():
    """Create a mock SentimentAnalysisRepository."""
    repository = AsyncMock(spec=SentimentAnalysisRepository)
    return repository


@pytest.fixture
def sentiment_service(mock_feddit_client, mock_sentiment_analyzer, mock_repository):
    """Create a SentimentService with mocked dependencies."""
    return SentimentService(
        feddit_client=mock_feddit_client,
        sentiment_analyzer=mock_sentiment_analyzer,
        sentiment_analysis_repository=mock_repository
    )


class TestSentimentService:
    """Test cases for SentimentService."""

    @pytest.mark.asyncio
    async def test_analyze_subfeddit_sentiment_success(
        self,
        sentiment_service,
        mock_feddit_client,
        mock_sentiment_analyzer,
        mock_repository
    ):
        """Test successful sentiment analysis of a subfeddit."""
        # Arrange
        subfeddit_name = "test_subfeddit"
        limit = 10
        start_time = datetime(2024, 1, 1)
        end_time = datetime(2024, 1, 2)
        
        # Mock subfeddits response
        mock_subfeddit = Subfeddit(
            id=1,
            username="test_user",
            title="test_subfeddit",
            description="A test subfeddit"
        )
        mock_feddit_client.get_subfeddits.return_value = [mock_subfeddit]
        
        # Mock comments response
        timestamp = datetime(2024, 1, 1, 12)
        mock_comment = Comment(
            id=1,
            subfeddit_id=1,
            username="user1",
            text="Positive comment",
            created_at=timestamp,
            updated_at=timestamp
        )
        mock_feddit_client.get_comments.return_value = [mock_comment]
        
        # Mock sentiment analyses
        mock_analyses = [
            SentimentAnalysis(
                id=1,
                comment_id=1,
                subfeddit_id=1,
                sentiment_score=0.8,
                sentiment_label="positive",
                created_at=datetime(2024, 1, 1, 12)
            )
        ]
        mock_sentiment_analyzer.analyze.return_value = mock_analyses
        
        # Act
        result = await sentiment_service.analyze_subfeddit_sentiment(
            subfeddit=subfeddit_name,
            limit=limit,
            start_time=start_time,
            end_time=end_time
        )
        
        # Assert
        assert result == mock_analyses
        mock_feddit_client.get_subfeddits.assert_called_once_with(limit=10, skip=0)
        mock_feddit_client.get_comments.assert_called_once_with(
            subfeddit_id=1,
            limit=limit
        )
        mock_sentiment_analyzer.analyze.assert_called_once_with([mock_comment])
        mock_repository.save.assert_called_once_with(mock_analyses[0])

    @pytest.mark.asyncio
    async def test_analyze_subfeddit_sentiment_subfeddit_not_found(
        self,
        sentiment_service,
        mock_feddit_client,
        mock_sentiment_analyzer,
        mock_repository
    ):
        """Test sentiment analysis when subfeddit is not found."""
        # Arrange
        subfeddit_name = "nonexistent_subfeddit"
        mock_feddit_client.get_subfeddits.return_value = []
        
        # Act & Assert
        with pytest.raises(ValueError, match=f"Subfeddit '{subfeddit_name}' not found"):
            await sentiment_service.analyze_subfeddit_sentiment(subfeddit=subfeddit_name)
        
        mock_feddit_client.get_subfeddits.assert_called_once_with(limit=10, skip=0)
        mock_feddit_client.get_comments.assert_not_called()
        mock_sentiment_analyzer.analyze.assert_not_called()
        mock_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_analyze_subfeddit_sentiment_api_error(
        self,
        sentiment_service,
        mock_feddit_client,
        mock_sentiment_analyzer,
        mock_repository
    ):
        """Test sentiment analysis when API call fails."""
        # Arrange
        subfeddit_name = "test_subfeddit"
        mock_feddit_client.get_subfeddits.side_effect = Exception("API Error")
        
        # Act & Assert
        with pytest.raises(Exception, match="API Error"):
            await sentiment_service.analyze_subfeddit_sentiment(subfeddit=subfeddit_name)
        
        mock_feddit_client.get_subfeddits.assert_called_once_with(limit=10, skip=0)
        mock_feddit_client.get_comments.assert_not_called()
        mock_sentiment_analyzer.analyze.assert_not_called()
        mock_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_analyze_subfeddit_sentiment_invalid_limit(
        self,
        sentiment_service,
        mock_feddit_client,
        mock_sentiment_analyzer,
        mock_repository
    ):
        """Test sentiment analysis with invalid limit values."""
        # Test limit < 1
        with pytest.raises(ValueError, match="Limit must be between 1 and 100"):
            await sentiment_service.analyze_subfeddit_sentiment(
                subfeddit="test_subfeddit",
                limit=0
            )
        
        # Test limit > 100
        with pytest.raises(ValueError, match="Limit must be between 1 and 100"):
            await sentiment_service.analyze_subfeddit_sentiment(
                subfeddit="test_subfeddit",
                limit=101
            )
        
        # Verify no API calls were made
        mock_feddit_client.get_subfeddits.assert_not_called()
        mock_feddit_client.get_comments.assert_not_called()
        mock_sentiment_analyzer.analyze.assert_not_called()
        mock_repository.save.assert_not_called()
