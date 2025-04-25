"""Tests for SentimentAnalysis domain entity."""

import pytest
from datetime import datetime
from pydantic_core._pydantic_core import ValidationError

from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis


def test_create_valid_sentiment_analysis():
    """Test creating a valid SentimentAnalysis."""
    now = datetime.now()
    analysis = SentimentAnalysis(
        id=1,
        comment_id=2,
        sentiment_score=0.5,
        sentiment_label="positive",
        created_at=now
    )
    
    assert analysis.id == 1
    assert analysis.comment_id == 2
    assert analysis.sentiment_score == 0.5
    assert analysis.sentiment_label == "positive"
    assert analysis.created_at == now


def test_create_invalid_sentiment_analysis():
    """Test creating an invalid SentimentAnalysis."""
    now = datetime.now()
    
    # Test invalid id
    with pytest.raises(ValidationError):
        SentimentAnalysis(
            id=0,  # Invalid: must be positive
            comment_id=2,
            sentiment_score=0.5,
            sentiment_label="positive",
            created_at=now
        )
    
    # Test invalid comment_id
    with pytest.raises(ValidationError):
        SentimentAnalysis(
            id=1,
            comment_id=0,  # Invalid: must be positive
            sentiment_score=0.5,
            sentiment_label="positive",
            created_at=now
        )
    
    # Test invalid sentiment_score
    with pytest.raises(ValidationError):
        SentimentAnalysis(
            id=1,
            comment_id=2,
            sentiment_score=1.5,  # Invalid: must be between -1 and 1
            sentiment_label="positive",
            created_at=now
        )
    
    # Test invalid sentiment_label
    with pytest.raises(ValidationError):
        SentimentAnalysis(
            id=1,
            comment_id=2,
            sentiment_score=0.5,
            sentiment_label="invalid",  # Invalid: not in allowed values
            created_at=now
        )
    
    # Test invalid datetime
    with pytest.raises(ValidationError):
        SentimentAnalysis(
            id=1,
            comment_id=2,
            sentiment_score=0.5,
            sentiment_label="positive",
            created_at="invalid_datetime"  # Invalid: not a datetime
        ) 