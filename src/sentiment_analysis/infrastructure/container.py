"""Dependency injection container."""

from sentiment_analysis.infrastructure.clients.feddit_client import FedditClient
from sentiment_analysis.infrastructure.repositories.feddit_subfeddit_repository import FedditSubfedditRepository
from sentiment_analysis.infrastructure.repositories.feddit_comment_repository import FedditCommentRepository
from sentiment_analysis.infrastructure.repositories.memory_sentiment_analysis_repository import MemorySentimentAnalysisRepository
from sentiment_analysis.application.use_cases.fetch_subfeddits import FetchSubfedditsUseCase
from sentiment_analysis.application.use_cases.fetch_comments import FetchCommentsUseCase
from sentiment_analysis.application.use_cases.analyze_sentiment import AnalyzeSentimentUseCase
from sentiment_analysis.application.services.sentiment_analysis_service import SentimentAnalysisService
from sentiment_analysis.config import FEDDIT_API_URL


class Container:
    """Dependency injection container."""
    
    def __init__(self, base_url: str = FEDDIT_API_URL):
        """Initialize the container.
        
        Args:
            base_url: Base URL of the Feddit API. Defaults to FEDDIT_API_URL from config.
        """
        self._base_url = base_url
        self._feddit_client = None
        self._subfeddit_repository = None
        self._comment_repository = None
        self._sentiment_analysis_repository = None
        self._fetch_subfeddits_use_case = None
        self._fetch_comments_use_case = None
        self._analyze_sentiment_use_case = None
        self._sentiment_analysis_service = None

    @property
    def feddit_client(self) -> FedditClient:
        """Get the FedditClient instance."""
        if self._feddit_client is None:
            self._feddit_client = FedditClient(base_url=self._base_url)
        return self._feddit_client

    @property
    def subfeddit_repository(self) -> FedditSubfedditRepository:
        """Get the SubfedditRepository instance."""
        if self._subfeddit_repository is None:
            self._subfeddit_repository = FedditSubfedditRepository(
                feddit_client=self.feddit_client
            )
        return self._subfeddit_repository

    @property
    def comment_repository(self) -> FedditCommentRepository:
        """Get the CommentRepository instance."""
        if self._comment_repository is None:
            self._comment_repository = FedditCommentRepository(
                feddit_client=self.feddit_client
            )
        return self._comment_repository

    @property
    def sentiment_analysis_repository(self) -> MemorySentimentAnalysisRepository:
        """Get the SentimentAnalysisRepository instance."""
        if self._sentiment_analysis_repository is None:
            self._sentiment_analysis_repository = MemorySentimentAnalysisRepository()
        return self._sentiment_analysis_repository

    @property
    def fetch_subfeddits_use_case(self) -> FetchSubfedditsUseCase:
        """Get the FetchSubfedditsUseCase instance."""
        if self._fetch_subfeddits_use_case is None:
            self._fetch_subfeddits_use_case = FetchSubfedditsUseCase(
                subfeddit_repository=self.subfeddit_repository
            )
        return self._fetch_subfeddits_use_case

    @property
    def fetch_comments_use_case(self) -> FetchCommentsUseCase:
        """Get the FetchCommentsUseCase instance."""
        if self._fetch_comments_use_case is None:
            self._fetch_comments_use_case = FetchCommentsUseCase(
                comment_repository=self.comment_repository
            )
        return self._fetch_comments_use_case

    @property
    def analyze_sentiment_use_case(self) -> AnalyzeSentimentUseCase:
        """Get the AnalyzeSentimentUseCase instance."""
        if self._analyze_sentiment_use_case is None:
            self._analyze_sentiment_use_case = AnalyzeSentimentUseCase(
                sentiment_analysis_repository=self.sentiment_analysis_repository
            )
        return self._analyze_sentiment_use_case

    @property
    def sentiment_analysis_service(self) -> SentimentAnalysisService:
        """Get the SentimentAnalysisService instance."""
        if self._sentiment_analysis_service is None:
            self._sentiment_analysis_service = SentimentAnalysisService(
                fetch_subfeddits_use_case=self.fetch_subfeddits_use_case,
                fetch_comments_use_case=self.fetch_comments_use_case,
                analyze_sentiment_use_case=self.analyze_sentiment_use_case
            )
        return self._sentiment_analysis_service

    async def close(self):
        """Close all resources."""
        if self._feddit_client is not None:
            await self._feddit_client.close() 