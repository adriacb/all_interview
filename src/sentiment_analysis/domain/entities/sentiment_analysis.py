"""Sentiment analysis entity."""

from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator
from pydantic_core._pydantic_core import ValidationError


class SentimentAnalysis(BaseModel):
    """Sentiment analysis entity."""
    id: int = Field(gt=0, description="Unique identifier for the analysis")
    comment_id: int = Field(gt=0, description="ID of the analyzed comment")
    subfeddit_id: int = Field(gt=0, description="ID of the subfeddit")
    sentiment_score: float = Field(
        ...,
        ge=-1.0,
        le=1.0,
        description="Sentiment score between -1.0 (negative) and 1.0 (positive)"
    )
    sentiment_label: Literal["positive", "neutral", "negative"] = Field(
        ...,
        description="Sentiment classification"
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the analysis was created"
    )

    @field_validator('sentiment_score')
    @classmethod
    def validate_sentiment_score(cls, v):
        """Validate that sentiment_score is between -1 and 1."""
        if not -1.0 <= v <= 1.0:
            raise ValidationError("Sentiment score must be between -1 and 1")
        return v

    @field_validator('created_at')
    @classmethod
    def validate_datetime(cls, v):
        """Validate that the value is a datetime."""
        if not isinstance(v, datetime):
            raise ValidationError("must be a datetime")
        return v 