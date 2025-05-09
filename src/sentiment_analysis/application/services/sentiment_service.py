"""Service for sentiment analysis operations."""
import structlog
from typing import List
from datetime import datetime
from sentiment_analysis.domain.entities.sentiment_analysis import SentimentAnalysis
from sentiment_analysis.domain.repositories.sentiment_analysis_repository import SentimentAnalysisRepository
from sentiment_analysis.infrastructure.clients.feddit_client import FedditClient
from sentiment_analysis.infrastructure.sentiment_analyzer import SentimentAnalyzer
from sentiment_analysis.application.use_cases.fetch_subfeddits import FetchSubfedditsUseCase
from sentiment_analysis.application.use_cases.fetch_comments import FetchCommentsUseCase
from sentiment_analysis.application.use_cases.analyze_sentiment import AnalyzeSentimentUseCase


class SentimentService:
    """Service for sentiment analysis operations.
    This service orchestrates the use cases for fetching subfeddits,
    fetching comments, and analyzing sentiment."""
    def __init__(
        self,
        feddit_client: FedditClient,
        sentiment_analyzer: SentimentAnalyzer,
        sentiment_analysis_repository: SentimentAnalysisRepository
    ):
        """Initialize the service.
        
        Args:
            feddit_client: Client for interacting with the Feddit API
            sentiment_analyzer: Analyzer for performing sentiment analysis
            sentiment_analysis_repository: Repository for storing sentiment analysis results
            
        Raises:
            ValueError: If any required dependency is not properly initialized
        """
        if not feddit_client:
            raise ValueError("FedditClient is required")
        if not sentiment_analyzer:
            raise ValueError("SentimentAnalyzer is required")
        if not sentiment_analysis_repository:
            raise ValueError("SentimentAnalysisRepository is required")
            
        self.feddit_client = feddit_client
        self.sentiment_analyzer = sentiment_analyzer
        self.sentiment_analysis_repository = sentiment_analysis_repository
        self.logger = structlog.get_logger(__name__)
        
        # Initialize use cases
        self.fetch_subfeddits = FetchSubfedditsUseCase(feddit_client)
        self.fetch_comments = FetchCommentsUseCase(feddit_client)
        self.analyze_sentiment = AnalyzeSentimentUseCase(
            sentiment_analyzer=sentiment_analyzer,
            sentiment_analysis_repository=sentiment_analysis_repository
        )

    async def analyze_subfeddit_sentiment(
        self,
        subfeddit: str,
        limit: int = 25,
        start_time: datetime | None = None,
        end_time: datetime | None = None
    ) -> List[SentimentAnalysis]:
        """Analyze sentiment of comments in a subfeddit.
        
        Args:
            subfeddit: Name of the subfeddit to analyze
            limit: Maximum number of comments to analyze (default: 25, min: 1, max: 100)
            start_time: Optional start time for filtering comments
            end_time: Optional end time for filtering comments
            
        Returns:
            List of sentiment analysis results
            
        Raises:
            ValueError: If the subfeddit is not found or if limit is invalid
            Exception: If an error occurs during analysis
        """
        if not 1 <= limit <= 100:
            raise ValueError("Limit must be between 1 and 100")
            
        self.logger.info(
            "Starting subfeddit sentiment analysis",
            subfeddit=subfeddit,
            limit=limit,
            start_time=start_time,
            end_time=end_time
        )
        
        try:
            # Fetch all subfeddits (there are only 3 total according to docs)
            subfeddits = await self.feddit_client.get_subfeddits(limit=10, skip=0)
            self.logger.info("Fetched subfeddits", subfeddits=subfeddits)
            matching_subfeddits = [s for s in subfeddits if s.title == subfeddit]
            if not matching_subfeddits:
                raise ValueError(f"Subfeddit '{subfeddit}' not found")
            
            subfeddit_id = matching_subfeddits[0].id
            
            # Get comments directly using get_comments
            comments = await self.feddit_client.get_comments(
                subfeddit_id=subfeddit_id,
                limit=limit
            )
            
            self.logger.info(
                "Fetched comments before filtering",
                comment_count=len(comments),
                comment_timestamps=[c.created_at for c in comments]
            )
            
            # Filter comments by time range if specified
            if start_time or end_time:
                filtered_comments = []
                for comment in comments:
                    self.logger.debug(
                        "Checking comment timestamp",
                        comment_id=comment.id,
                        created_at=comment.created_at,
                        start_time=start_time,
                        end_time=end_time,
                        matches_start=not start_time or comment.created_at >= start_time,
                        matches_end=not end_time or comment.created_at <= end_time
                    )
                    if (
                        (not start_time or comment.created_at >= start_time) and
                        (not end_time or comment.created_at <= end_time)
                    ):
                        filtered_comments.append(comment)
                comments = filtered_comments
            
            self.logger.info(
                "Comments after filtering",
                comment_count=len(comments),
                comment_timestamps=[c.created_at for c in comments]
            )
            
            if not comments:
                self.logger.info("No comments found in time range")
                return []
            
            # Analyze sentiment
            analyses = await self.sentiment_analyzer.analyze(comments)
            
            # Save analyses to repository
            for analysis in analyses:
                self.sentiment_analysis_repository.save(analysis)
            
            self.logger.info(
                "Successfully analyzed subfeddit sentiment",
                subfeddit=subfeddit,
                analysis_count=len(analyses)
            )
            
            return analyses
        except ValueError as e:
            # Re-raise ValueError for subfeddit not found or invalid limit
            self.logger.error(
                "Error in sentiment analysis",
                subfeddit=subfeddit,
                error=str(e)
            )
            raise
        except Exception as e:
            # Log and re-raise other errors
            self.logger.error(
                "Failed to analyze subfeddit sentiment",
                error=str(e),
                subfeddit=subfeddit
            )
            raise
