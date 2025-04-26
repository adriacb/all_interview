"""Tests for AnalyzeSentimentUseCase."""

import pytest
from unittest.mock import AsyncMock
from datetime import datetime

from sentiment_analysis.application.use_cases.analyze_sentiment import AnalyzeSentimentUseCase
from sentiment_analysis.domain.entities.comment import Comment
from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis


class TestAnalyzeSentimentUseCase:
    """Test cases for AnalyzeSentimentUseCase."""

    @pytest.fixture
    def mock_analyzer(self):
        """Create a mock sentiment analyzer."""
        return AsyncMock()

    @pytest.fixture
    def mock_repository(self):
        """Create a mock sentiment analysis repository."""
        return AsyncMock()

    @pytest.fixture
    def use_case(self, mock_analyzer, mock_repository):
        """Create a use case instance with mocked dependencies."""
        return AnalyzeSentimentUseCase(
            sentiment_analyzer=mock_analyzer,
            sentiment_analysis_repository=mock_repository
        )

    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_analyzer, mock_repository):
        """Test successful execution of the use case."""
        # Mock input comments
        comments = [
            Comment(
                id=1,
                subfeddit_id=2,
                username="test_user",
                text="Test comment",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]

        # Mock analyzer response
        mock_analysis = SentimentAnalysis(
            id=1,
            comment_id=1,
            subfeddit_id=2,
            sentiment_score=0.5,
            sentiment_label="positive",
            created_at=datetime.now()
        )
        mock_analyzer.analyze.return_value = [mock_analysis]

        # Mock repository to return a saved entity
        saved_entity = SentimentAnalysis(
            id=1,
            comment_id=1,
            subfeddit_id=2,
            sentiment_score=0.5,
            sentiment_label="positive",
            created_at=datetime.now()
        )
        mock_repository.save.return_value = saved_entity

        # Execute use case
        result = await use_case.execute(comments)

        # Verify result
        assert len(result) == 1
        assert result[0].id == 1
        assert result[0].comment_id == 1
        assert result[0].subfeddit_id == 2
        assert result[0].sentiment_score == 0.5
        assert result[0].sentiment_label == "positive"

        # Verify analyzer was called
        mock_analyzer.analyze.assert_called_once_with(comments)

        # Verify repository was called
        mock_repository.save.assert_called_once_with(mock_analysis)

    @pytest.mark.asyncio
    async def test_execute_error(self, use_case, mock_analyzer):
        """Test error handling."""
        # Mock input comments
        comments = [
            Comment(
                id=1,
                subfeddit_id=2,
                username="test_user",
                text="Test comment",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]

        # Mock analyzer to raise an error
        mock_analyzer.analyze.side_effect = Exception("Test error")

        # Execute use case and expect an exception
        with pytest.raises(Exception) as exc_info:
            await use_case.execute(comments)
        
        assert str(exc_info.value) == "Test error"
