"""Tests for SentimentAnalyzer."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock, ANY

from sentiment_analysis.infrastructure.sentiment_analyzer import SentimentAnalyzer


class TestSentimentAnalyzer:
    """Test cases for SentimentAnalyzer."""

    @pytest.fixture
    def mock_openai_response(self):
        """Create a mock OpenAI response."""
        mock_response = MagicMock()
        mock_response.output_text = "0.5"
        return mock_response

    @pytest.fixture
    def analyzer(self):
        """Create a SentimentAnalyzer instance with mock API key."""
        return SentimentAnalyzer(api_key="test-key")

    @pytest.mark.asyncio
    async def test_analyze_success(self, analyzer, mock_openai_response):
        """Test successful sentiment analysis."""
        # Mock OpenAI client
        mock_create = AsyncMock(return_value=mock_openai_response)
        with patch.object(analyzer.client.responses, 'create', mock_create):
            # Test with any text
            text = "I love this product!"
            result = await analyzer.analyze(text)
            
            # Verify result
            assert isinstance(result, float)
            assert result == 0.5
            
            # Verify the API was called with correct parameters
            mock_create.assert_called_once_with(
                model="gpt-4o-mini",
                instructions="You are a sentiment analysis tool that returns only numbers between -1.0 and 1.0.",
                input=ANY
            )

    @pytest.mark.asyncio
    async def test_analyze_error(self, analyzer):
        """Test error handling."""
        # Mock OpenAI client to raise an error
        mock_create = AsyncMock(side_effect=Exception("Test error"))
        with patch.object(analyzer.client.responses, 'create', mock_create):
            # Test with any text
            text = "test"
            
            # Expect an exception
            with pytest.raises(Exception) as exc_info:
                await analyzer.analyze(text)
            
            assert str(exc_info.value) == "Test error"

    @pytest.mark.asyncio
    async def test_analyze_invalid_response(self, analyzer):
        """Test handling of invalid API response."""
        # Mock OpenAI client to return invalid response
        mock_invalid_response = MagicMock()
        mock_invalid_response.output_text = "invalid"
        mock_create = AsyncMock(return_value=mock_invalid_response)
        
        with patch.object(analyzer.client.responses, 'create', mock_create):
            # Test with any text
            text = "test"
            
            # Expect an exception
            with pytest.raises(ValueError):
                await analyzer.analyze(text)

    def test_init_without_api_key(self):
        """Test initialization without API key."""
        # Remove API key from environment
        with patch.dict('os.environ', {}, clear=True):
            # Expect an exception
            with pytest.raises(ValueError):
                SentimentAnalyzer() 