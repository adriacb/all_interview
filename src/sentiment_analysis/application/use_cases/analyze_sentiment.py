"""Use case for analyzing sentiment of comments."""
from typing import List

from sentiment_analysis.domain.entities.comment import Comment
from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis
from sentiment_analysis.domain.repositories.sentiment_analysis_repository import SentimentAnalysisRepository
from sentiment_analysis.infrastructure.sentiment_analyzer import SentimentAnalyzer
from sentiment_analysis.logger import configure_logger


class AnalyzeSentimentUseCase:
    """Use case for analyzing sentiment of comments.

    This use case handles the business logic for analyzing the sentiment of comments
    and storing the results.
    """

    def __init__(
        self,
        sentiment_analyzer: SentimentAnalyzer,
        sentiment_analysis_repository: SentimentAnalysisRepository
    ):
        """Initialize the use case.

        Args:
            sentiment_analyzer: Analyzer for performing sentiment analysis.
            sentiment_analysis_repository: Repository for storing sentiment analysis results.
        """
        self.sentiment_analyzer = sentiment_analyzer
        self.sentiment_analysis_repository = sentiment_analysis_repository
        self.logger = configure_logger().bind(use_case="analyze_sentiment")

    def _get_sentiment_label(self, score: float) -> str:
        """Get sentiment label based on score.

        Args:
            score: Sentiment score between -1 and 1.

        Returns:
            Sentiment label: "positive" or "negative".

        Raises:
            ValueError: If score is exactly 0.0.
        """
        if score > 0.0:
            return "positive"
        elif score < 0.0:
            return "negative"
        raise ValueError("Score cannot be exactly 0.0 for binary classification")

    async def execute(self, comments: List[Comment]) -> List[SentimentAnalysis]:
        """Execute the use case.

        Args:
            comments: List of comments to analyze.

        Returns:
            List of SentimentAnalysis objects.

        Raises:
            Exception: If an error occurs while analyzing sentiment.
        """
        self.logger.info(
            "Analyzing sentiment",
            comment_count=len(comments)
        )
        try:
            # Analyze sentiment for all comments
            analyses = await self.sentiment_analyzer.analyze(comments)
            
            # Save analyses to repository
            for analysis in analyses:
                await self.sentiment_analysis_repository.save(analysis)
            
            self.logger.info(
                "Successfully analyzed sentiment",
                analysis_count=len(analyses)
            )
            return analyses
        except Exception as e:
            self.logger.error(
                "Failed to analyze sentiment",
                error=str(e)
            )
            raise
