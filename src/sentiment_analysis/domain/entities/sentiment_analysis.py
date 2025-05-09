"""Sentiment analysis entity."""

from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator


class SentimentAnalysis(BaseModel):
    """Sentiment analysis entity."""
    id: int = Field(gt=0, description="Unique identifier for the analysis")
    comment_id: int = Field(gt=0, description="ID of the analyzed comment")
    comment_text: str = Field(..., description="Text content of the analyzed comment")
    subfeddit_id: int = Field(gt=0, description="ID of the subfeddit")
    sentiment_score: float = Field(
        ...,
        ge=-1.0,
        le=1.0,
        description="Sentiment score between -1.0 (negative) and 1.0 (positive)"
    )
    sentiment_label: Literal["positive", "negative"] = Field(
        ...,
        description="Sentiment classification"
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the analysis was created"
    )

    @field_validator("comment_text")
    def validate_comment_text(cls, v):
        """Validate comment text."""
        if not v:
            raise ValueError("Comment text cannot be empty")
        return v

    @field_validator("sentiment_label")
    def validate_sentiment_label(cls, v, values):
        """Validate sentiment label and ensure consistency with score."""
        if "sentiment_score" in values.data:
            score = values.data["sentiment_score"]
            if score > 0.0 and v != "positive":
                raise ValueError("Score-label mismatch: positive score with non-positive label")
            if score < 0.0 and v != "negative":
                raise ValueError("Score-label mismatch: negative score with non-negative label")
            if score == 0.0:
                raise ValueError("Score cannot be exactly 0.0 for binary classification")
        return v

    @field_validator("created_at")
    def validate_created_at(cls, v):
        """Validate created_at datetime."""
        if not isinstance(v, datetime):
            raise ValueError("created_at must be a datetime object")
        return v
