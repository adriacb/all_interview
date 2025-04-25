"""Tests for AnalyzeSentimentUseCase."""

import pytest
from unittest.mock import AsyncMock, patch
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
        """Create a mock repository."""
        return AsyncMock()

    @pytest.fixture
    def use_case(self, mock_analyzer, mock_repository):
        """Create a use case instance."""
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
        mock_analyzer.analyze.return_value = 0.5

        # Mock repository to return a created entity
        created_entity = SentimentAnalysis(
            id=1,
            comment_id=1,
            subfeddit_id=2,
            sentiment_score=0.5,
            sentiment_label="positive",
            created_at=datetime.now()
        )
        mock_repository.create.return_value = created_entity

        # Execute use case
        result = await use_case.execute(comments)

        # Verify results
        assert len(result) == 1
        assert isinstance(result[0], SentimentAnalysis)
        assert result[0].id == 1
        assert result[0].comment_id == 1
        assert result[0].subfeddit_id == 2
        assert result[0].sentiment_score == 0.5
        assert result[0].sentiment_label == "positive"
        assert isinstance(result[0].created_at, datetime)

        # Verify analyzer call
        mock_analyzer.analyze.assert_called_once_with("Test comment")

        # Verify repository call
        mock_repository.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_error(self, use_case, mock_analyzer, mock_repository):
        """Test error handling in the use case."""
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
        mock_analyzer.analyze.assert_called_once()
        mock_repository.create.assert_not_called() 