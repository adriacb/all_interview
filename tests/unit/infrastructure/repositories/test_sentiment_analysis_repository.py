import pytest
from datetime import datetime

from sentiment_analysis.infrastructure.repositories.sentiment_analysis_repository import SentimentAnalysisRepository
from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis


class TestSentimentAnalysisRepository:

    @pytest.mark.asyncio
    async def test_save_requires_comment_text(self):
        """Test that save requires comment text."""
        # Arrange
        repository = SentimentAnalysisRepository()
        # Create a valid analysis first
        analysis = SentimentAnalysis(
            id=1,
            comment_id=1,
            comment_text="Initial text",  # Start with valid text
            subfeddit_id=1,
            sentiment_score=0.5,
            sentiment_label="positive",
            created_at=datetime.now()
        )
        
        # Modify the comment_text after creation to bypass Pydantic validation
        analysis.comment_text = ""  # Set to empty string

        # Act & Assert
        with pytest.raises(ValueError, match="Comment text is required for sentiment analysis"):
            await repository.save(analysis)

    @pytest.mark.asyncio
    async def test_save_with_valid_comment_text(self):
        """Test that save works with valid comment text."""
        # Arrange
        repository = SentimentAnalysisRepository()
        analysis = SentimentAnalysis(
            id=1,
            comment_id=1,
            comment_text="Valid comment text",
            subfeddit_id=1,
            sentiment_score=0.5,
            sentiment_label="positive",
            created_at=datetime.now()
        )

        # Act
        await repository.save(analysis)

        # Assert
        saved_analysis = await repository.get_by_comment_id(1)
        assert saved_analysis is not None
        assert saved_analysis.comment_text == "Valid comment text"
