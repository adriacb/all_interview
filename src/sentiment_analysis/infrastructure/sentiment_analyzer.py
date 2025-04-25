"""Sentiment analyzer using OpenAI GPT-4o mini."""

from typing import Optional
import os
from openai import AsyncOpenAI

from sentiment_analysis.logger import configure_logger


class SentimentAnalyzer:
    """Analyzer for performing sentiment analysis on text.

    This class uses OpenAI's GPT-4o mini to analyze the sentiment of text and return a polarity score.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the sentiment analyzer.

        Args:
            api_key: OpenAI API key. If not provided, will use OPENAI_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.logger = configure_logger().bind(service="sentiment_analyzer")

    async def analyze(self, text: str) -> float:
        """Analyze the sentiment of the given text.

        Args:
            text: The text to analyze.

        Returns:
            A polarity score between -1.0 (negative) and 1.0 (positive).

        Raises:
            Exception: If an error occurs during analysis.
        """
        self.logger.info(
            "Analyzing sentiment",
            text_length=len(text)
        )
        try:
            # Create prompt for sentiment analysis
            prompt = f"""
            Analyze the sentiment of the following text and return a single number between -1.0 and 1.0,
            where -1.0 is extremely negative, 0 is neutral, and 1.0 is extremely positive.
            Only return the number, nothing else.

            Text: "{text}"
            """

            # Call OpenAI API
            response = await self.client.responses.create(
                model="gpt-4o-mini",
                instructions="You are a sentiment analysis tool that returns only numbers between -1.0 and 1.0.",
                input=prompt
            )
            
            # Extract and parse the score
            score = float(response.output_text.strip())
            
            self.logger.info(
                "Successfully analyzed sentiment",
                polarity=score
            )
            return score
        except Exception as e:
            self.logger.error(
                "Failed to analyze sentiment",
                error=str(e)
            )
            raise 