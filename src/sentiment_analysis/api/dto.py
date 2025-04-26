"""API data transfer objects."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis


class SentimentAnalysisResponseDTO(BaseModel):
    """API response DTO for sentiment analysis."""
    analyses: List[SentimentAnalysis] = Field(
        ...,
        description="List of sentiment analyses",
        example=[
            {
                "id": 1,
                "comment_id": 1,
                "subfeddit_id": 1,
                "sentiment_score": 0.8,
                "sentiment_label": "positive",
                "created_at": "2024-01-01T00:00:00"
            }
        ]
    )


class SentimentAnalysisRequestDTO(BaseModel):
    """API request DTO for sentiment analysis."""
    limit: int = Field(
        default=25,
        ge=1,
        le=100,
        description="Maximum number of comments to analyze"
    )
    start_time: Optional[datetime] = Field(
        default=None,
        description="Optional start time for filtering comments"
    )
    end_time: Optional[datetime] = Field(
        default=None,
        description="Optional end time for filtering comments"
    )
    sort_by_score: bool = Field(
        default=False,
        description="Whether to sort results by sentiment score"
    )
