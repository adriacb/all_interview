"""SentimentAnalysis domain entity."""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from pydantic_core._pydantic_core import ValidationError
from typing import Literal


class SentimentAnalysis(BaseModel):
    """SentimentAnalysis domain entity."""
    
    id: int = Field(gt=0, description="Unique identifier for the sentiment analysis")
    comment_id: int = Field(gt=0, description="ID of the comment being analyzed")
    subfeddit_id: int = Field(gt=0, description="ID of the subfeddit containing the comment")
    sentiment_score: float = Field(ge=-1.0, le=1.0, description="Sentiment score between -1 and 1")
    sentiment_label: Literal["positive", "neutral", "negative"] = Field(description="Type of sentiment detected")
    created_at: datetime = Field(description="Creation timestamp")
    
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
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "comment_id": 1,
                "subfeddit_id": 1,
                "sentiment_score": 0.5,
                "sentiment_label": "positive",
                "created_at": "2024-01-01T00:00:00"
            }
        } 