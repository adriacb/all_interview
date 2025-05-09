"""Tests for SentimentAnalyzer."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock, ANY
from datetime import datetime
from openai import OpenAIError

from sentiment_analysis.infrastructure.sentiment_analyzer import SentimentAnalyzer, OutputFormat
from sentiment_analysis.domain.entities.comment import Comment


class MockResponse:
    """Mock response for OpenAI API."""
    def __init__(self, output_parsed):
        self.output_parsed = output_parsed


@pytest.fixture
def mock_openai_client():
    """Create a mock OpenAI client."""
    mock_client = MagicMock()
    mock_client.responses = MagicMock()
    mock_client.responses.parse = AsyncMock(return_value=MockResponse(
        output_parsed=OutputFormat(
            sentiment_score=0.5,
            sentiment_label="positive"
        )
    ))
    return mock_client


@pytest.fixture
def analyzer(mock_openai_client):
    """Create a SentimentAnalyzer instance with mock client."""
    with patch('sentiment_analysis.infrastructure.sentiment_analyzer.AsyncOpenAI', return_value=mock_openai_client):
        analyzer = SentimentAnalyzer(api_key="test-key")
        return analyzer


class TestSentimentAnalyzer:
    """Test cases for SentimentAnalyzer."""

    @pytest.fixture
    def mock_openai_response(self):
        """Create a mock OpenAI response."""
        mock_response = MagicMock()
        mock_response.output_parsed.sentiment_score = 0.5
        mock_response.output_parsed.sentiment_label = "positive"
        return mock_response

    @pytest.fixture
    def mock_comment(self):
        """Create a mock Comment object."""
        return Comment(
            id=1,
            subfeddit_id=1,
            username="test_user",
            text="I love this product!",
            created_at=datetime.now()
        )

    @pytest.mark.asyncio
    async def test_analyze_success(self, analyzer, mock_openai_response, mock_comment):
        """Test successful sentiment analysis."""
        # Mock OpenAI client
        mock_parse = AsyncMock(return_value=mock_openai_response)
        with patch.object(analyzer.client.responses, 'parse', mock_parse):
            # Test with a Comment object
            result = await analyzer.analyze([mock_comment])
            
            # Verify result
            assert len(result) == 1
            assert result[0].sentiment_score == 0.5
            assert result[0].sentiment_label == "positive"
            assert result[0].comment_id == mock_comment.id
            assert result[0].subfeddit_id == mock_comment.subfeddit_id
            
            # Verify the API was called with correct parameters
            mock_parse.assert_called_once_with(
                model="gpt-4o-mini",
                input=[
                    {
                        "role": "system",
                        "content": "You are a sentiment analyst professional. Analyze the following text and return a sentiment score between -1.0 and 1.0, where -1.0 is extremely negative and 1.0 is extremely positive. The score cannot be exactly 0.0 as we use binary classification: positive (>0.0) or negative (<0.0).",
                    },
                    {"role": "user", "content": mock_comment.text},
                ],
                text_format=ANY
            )

    @pytest.mark.asyncio
    async def test_analyze_error(self, analyzer, mock_comment):
        """Test error handling."""
        # Mock OpenAI client to raise an error
        mock_parse = AsyncMock(side_effect=Exception("Test error"))
        with patch.object(analyzer.client.responses, 'parse', mock_parse):
            # Test with a Comment object
            with pytest.raises(Exception) as exc_info:
                await analyzer.analyze([mock_comment])
            
            assert str(exc_info.value) == "Test error"

    @pytest.mark.asyncio
    async def test_analyze_invalid_response(self, analyzer, mock_comment):
        """Test handling of invalid API response."""
        # Mock OpenAI client to return invalid response
        mock_invalid_response = MagicMock()
        mock_invalid_response.output_parsed.sentiment_score = "invalid"
        mock_invalid_response.output_parsed.sentiment_label = "invalid"
        mock_parse = AsyncMock(return_value=mock_invalid_response)
        
        with patch.object(analyzer.client.responses, 'parse', mock_parse):
            # Test with a Comment object
            with pytest.raises(ValueError):
                await analyzer.analyze([mock_comment])

    def test_init_without_api_key(self):
        """Test initialization without API key."""
        # Create a mock AsyncOpenAI class that raises OpenAIError when initialized without api_key
        class MockAsyncOpenAI:
            def __init__(self, *, api_key=None, **kwargs):
                if api_key is None:
                    raise OpenAIError("API key is required")
                self.api_key = api_key
                self.responses = MagicMock()

        # Remove API key from environment and mock config
        with patch.dict('os.environ', {}, clear=True), \
             patch('sentiment_analysis.infrastructure.sentiment_analyzer.OPENAI_API_KEY', None), \
             patch('sentiment_analysis.infrastructure.sentiment_analyzer.AsyncOpenAI', MockAsyncOpenAI):
            # Expect an exception
            with pytest.raises(ValueError, match="API key is required"):
                SentimentAnalyzer()

    @pytest.mark.asyncio
    async def test_analyze_single_comment_includes_comment_text(self, analyzer, mock_comment):
        """Test that analyze_single_comment includes comment text in the analysis."""
        # Act
        analysis = await analyzer._analyze_single_comment(mock_comment)

        # Assert
        assert analysis.comment_text == mock_comment.text
        assert analysis.sentiment_score == 0.5
        assert analysis.sentiment_label == "positive"

    @pytest.mark.asyncio
    async def test_analyze_batch_includes_comment_text(self, analyzer):
        """Test that analyze includes comment text for all comments in a batch."""
        # Arrange
        comments = [
            Comment(
                id=1,
                text="First comment",
                subfeddit_id=1,
                username="test_user",
                created_at=datetime.now()
            ),
            Comment(
                id=2,
                text="Second comment",
                subfeddit_id=1,
                username="test_user",
                created_at=datetime.now()
            )
        ]

        # Act
        analyses = await analyzer.analyze(comments)

        # Assert
        assert len(analyses) == 2
        assert analyses[0].comment_text == "First comment"
        assert analyses[1].comment_text == "Second comment"
