"""Sentiment analyzer using OpenAI's API."""
from typing import List, Optional
from openai import AsyncOpenAI, OpenAIError
from pydantic import BaseModel, Field
from sentiment_analysis.domain.entities.comment import Comment
from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis
from sentiment_analysis.logger import configure_logger
from sentiment_analysis.config import OPENAI_API_KEY
from datetime import datetime

logger = configure_logger().bind(service="sentiment_analyzer")


class OutputFormat(BaseModel):
    """Output format for the sentiment analysis."""
    sentiment_score: float = Field(description="The sentiment score of the comment, between -1.0 and 1.0")
    sentiment_label: str = Field(description="The sentiment label of the comment, either 'positive' or 'negative'")


class SentimentAnalyzer:
    """Analyzes sentiment of comments using OpenAI's API."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the sentiment analyzer.
        
        Args:
            api_key: OpenAI API key. If not provided, will be loaded from environment.

        Raises:
            ValueError: If no API key is provided and OPENAI_API_KEY is not set.
        """
        self.api_key = api_key or OPENAI_API_KEY
        try:
            self.client = AsyncOpenAI(api_key=self.api_key)
        except OpenAIError as e:
            raise ValueError("API key is required") from e
        self.logger = configure_logger().bind(service="sentiment_analyzer")

    async def analyze(self, comments: List[Comment]) -> List[SentimentAnalysis]:
        """Analyze sentiment for a list of comments.

        Args:
            comments: List of comments to analyze.

        Returns:
            List of SentimentAnalysis objects.

        Raises:
            Exception: If sentiment analysis fails.
        """
        self.logger.info(
            "Analyzing sentiment for comments",
            comment_count=len(comments)
        )
        
        analyses = []
        for comment in comments:
            try:
                response = await self.client.responses.parse(
                    model="gpt-4o-mini",
                    input=[
                        {
                            "role": "system",
                            "content": "You are a sentiment analyst professional. Analyze the following text and return a single number between -1.0 and 1.0, where -1.0 is extremely negative, 0.0 is neutral, and 1.0 is extremely positive.",
                        },
                        {"role": "user", "content": comment.text},
                    ],
                    text_format=OutputFormat
                )
                output = response.output_parsed
                self.logger.info("Response from OpenAI", parsed_response=output)

                score = output.sentiment_score
                label = output.sentiment_label

                # Create sentiment analysis
                analysis = SentimentAnalysis(
                    id=comment.id,  # Use comment ID as analysis ID
                    comment_id=comment.id,
                    subfeddit_id=comment.subfeddit_id,
                    sentiment_score=score,
                    sentiment_label=label,
                    created_at=datetime.now()
                )
                
                analyses.append(analysis)
                self.logger.info(
                    "Successfully analyzed comment",
                    comment_id=comment.id,
                    sentiment_score=analysis.sentiment_score,
                    sentiment_label=analysis.sentiment_label
                )
            except Exception as e:
                self.logger.error(
                    "Failed to analyze comment",
                    error=str(e),
                    comment_id=comment.id
                )
                raise
        
        self.logger.info(
            "Successfully analyzed all comments",
            analysis_count=len(analyses)
        )
        return analyses
