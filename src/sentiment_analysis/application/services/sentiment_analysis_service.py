"""SentimentAnalysisService implementation."""
import asyncio

from sentiment_analysis.domain.entities.comment import Comment
from sentiment_analysis.domain.entities.subfeddit import Subfeddit
from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis
from sentiment_analysis.application.use_cases.fetch_subfeddits import FetchSubfedditsUseCase
from sentiment_analysis.application.use_cases.fetch_comments import FetchCommentsUseCase
from sentiment_analysis.application.use_cases.analyze_sentiment import AnalyzeSentimentUseCase
from sentiment_analysis.logger import configure_logger


class SentimentAnalysisService:
    """Service for analyzing sentiment of Feddit comments."""
    
    def __init__(
        self,
        fetch_subfeddits_use_case: FetchSubfedditsUseCase,
        fetch_comments_use_case: FetchCommentsUseCase,
        analyze_sentiment_use_case: AnalyzeSentimentUseCase,
        interval_seconds: int = 60
    ):
        """Initialize the service.
        
        Args:
            fetch_subfeddits_use_case: Use case for fetching subfeddits
            fetch_comments_use_case: Use case for fetching comments
            analyze_sentiment_use_case: Use case for analyzing sentiment
            interval_seconds: Interval between analysis runs in seconds
        """
        self._fetch_subfeddits_use_case = fetch_subfeddits_use_case
        self._fetch_comments_use_case = fetch_comments_use_case
        self._analyze_sentiment_use_case = analyze_sentiment_use_case
        self._interval_seconds = interval_seconds
        self._logger = configure_logger().bind(service="sentiment_analysis")
        self._running = False

    async def start(self):
        """Start the service."""
        self._running = True
        self._logger.info("Starting sentiment analysis service")
        
        while self._running:
            try:
                await self._analyze_subfeddits()
            except Exception as e:
                self._logger.error(
                    "Error in sentiment analysis service",
                    error=str(e)
                )
            
            await asyncio.sleep(self._interval_seconds)

    async def stop(self):
        """Stop the service."""
        self._running = False
        self._logger.info("Stopping sentiment analysis service")

    async def _analyze_subfeddits(self):
        """Analyze sentiment of comments in all subfeddits."""
        self._logger.info("Starting subfeddit analysis")
        
        subfeddits = await self._fetch_subfeddits_use_case.execute()
        self._logger.info(
            "Fetched subfeddits",
            count=len(subfeddits)
        )
        
        for subfeddit in subfeddits:
            try:
                await self._analyze_subfeddit(subfeddit)
            except Exception as e:
                self._logger.error(
                    "Error analyzing subfeddit",
                    error=str(e),
                    subfeddit_id=subfeddit.id
                )

    async def _analyze_subfeddit(self, subfeddit: Subfeddit):
        """Analyze sentiment of comments in a subfeddit.
        
        Args:
            subfeddit: Subfeddit to analyze
        """
        self._logger.info(
            "Analyzing subfeddit",
            subfeddit_id=subfeddit.id,
            title=subfeddit.title
        )
        
        comments = await self._fetch_comments_use_case.execute(
            subfeddit_id=subfeddit.id
        )
        self._logger.info(
            "Fetched comments",
            count=len(comments),
            subfeddit_id=subfeddit.id
        )
        
        for comment in comments:
            try:
                await self._analyze_comment(comment)
            except Exception as e:
                self._logger.error(
                    "Error analyzing comment",
                    error=str(e),
                    comment_id=comment.id,
                    subfeddit_id=subfeddit.id
                )

    async def _analyze_comment(self, comment: Comment) -> SentimentAnalysis:
        """Analyze sentiment of a comment.
        
        Args:
            comment: Comment to analyze
            
        Returns:
            SentimentAnalysis entity
        """
        self._logger.info(
            "Analyzing comment",
            comment_id=comment.id,
            subfeddit_id=comment.subfeddit_id
        )
        
        analyses = await self._analyze_sentiment_use_case.execute([comment])
        analysis = analyses[0]  # Get the first (and only) analysis
        
        self._logger.info(
            "Completed comment analysis",
            comment_id=comment.id,
            subfeddit_id=comment.subfeddit_id,
            sentiment_score=analysis.sentiment_score,
            sentiment_label=analysis.sentiment_label
        )
        
        return analysis
