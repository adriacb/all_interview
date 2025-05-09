"""Sentiment analyzer using OpenAI's API."""
from typing import List, Optional
from openai import AsyncOpenAI, OpenAIError
from pydantic import BaseModel, Field
from sentiment_analysis.domain.entities.comment import Comment
from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis
from sentiment_analysis.logger import configure_logger
from sentiment_analysis.config import OPENAI_API_KEY, SENTIMENT_ANALYSIS_BATCH_SIZE
from datetime import datetime
import asyncio

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
            ValueError: If the API response is invalid.
        """
        batch_size = SENTIMENT_ANALYSIS_BATCH_SIZE
        self.logger.info(
            "Starting batch processing of comments",
            total_comments=len(comments),
            batch_size=batch_size
        )
        
        if SENTIMENT_ANALYSIS_BATCH_SIZE > len(comments):
            self.logger.warning(
                "Batch size is greater than the number of comments",
                batch_size=batch_size,
                comment_count=len(comments)
            )
            batch_size = len(comments)

        all_analyses = []
        
        # Process comments in batches
        for i in range(0, len(comments), SENTIMENT_ANALYSIS_BATCH_SIZE):
            batch = comments[i:i + SENTIMENT_ANALYSIS_BATCH_SIZE]
            self.logger.info(
                "Processing batch",
                batch_number=i // SENTIMENT_ANALYSIS_BATCH_SIZE + 1,
                batch_size=len(batch)
            )
            
            # Create tasks for this batch
            batch_tasks = [
                self._analyze_single_comment(comment)
                for comment in batch
            ]
            
            # Process this batch in parallel
            batch_analyses = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            # Handle results from this batch
            for analysis, comment in zip(batch_analyses, batch):
                if isinstance(analysis, Exception):
                    # Re-raise the first exception we encounter
                    raise analysis
                all_analyses.append(analysis)
                    
            self.logger.info(
                "Processed batch of comments",
                batch_size=len(batch),
                successful_analyses=len(batch)
            )
        
        self.logger.info(
            "Successfully analyzed all comments",
            total_analyses=len(all_analyses)
        )
        return all_analyses

    async def _analyze_single_comment(self, comment: Comment) -> SentimentAnalysis:
        """Analyze a single comment.
        
        Args:
            comment: The comment to analyze.
            
        Returns:
            SentimentAnalysis object.
            
        Raises:
            Exception: If sentiment analysis fails.
            ValueError: If the API response is invalid.
        """
        try:
            response = await self.client.responses.parse(
                model="gpt-4o-mini",
                input=[
                    {
                        "role": "system",
                        "content": "You are a sentiment analyst professional. Analyze the following text and return a sentiment score between -1.0 and 1.0, where -1.0 is extremely negative and 1.0 is extremely positive. The score cannot be exactly 0.0 as we use binary classification: positive (>0.0) or negative (<0.0).",
                    },
                    {"role": "user", "content": comment.text},
                ],
                text_format=OutputFormat
            )
            output = response.output_parsed
            self.logger.debug("Response from OpenAI", parsed_response=output)

            # Create sentiment analysis
            analysis = SentimentAnalysis(
                id=comment.id,  # Use comment ID as analysis ID
                comment_id=comment.id,
                comment_text=comment.text,
                subfeddit_id=comment.subfeddit_id,
                sentiment_score=output.sentiment_score,
                sentiment_label=output.sentiment_label,
                created_at=datetime.now()
            )
            
            self.logger.debug(
                "Successfully analyzed comment",
                comment_id=comment.id,
                sentiment_score=analysis.sentiment_score,
                sentiment_label=analysis.sentiment_label
            )
            return analysis
        except Exception as e:
            self.logger.error(
                "Failed to analyze comment",
                error=str(e),
                comment_id=comment.id
            )
            raise
