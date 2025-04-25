"""Dependency injection for FastAPI application."""

from fastapi import Depends

from sentiment_analysis.application.services.sentiment_service import SentimentService
from sentiment_analysis.infrastructure.clients.feddit_client import FedditClient
from sentiment_analysis.infrastructure.sentiment_analyzer import SentimentAnalyzer
from sentiment_analysis.infrastructure.repositories.sentiment_analysis_repository import SentimentAnalysisRepository


def get_feddit_client() -> FedditClient:
    """Get FedditClient instance."""
    return FedditClient()


def get_sentiment_analyzer() -> SentimentAnalyzer:
    """Get SentimentAnalyzer instance."""
    return SentimentAnalyzer()


def get_sentiment_analysis_repository() -> SentimentAnalysisRepository:
    """Get SentimentAnalysisRepository instance."""
    return SentimentAnalysisRepository()


def get_sentiment_service(
    feddit_client: FedditClient = Depends(get_feddit_client),
    sentiment_analyzer: SentimentAnalyzer = Depends(get_sentiment_analyzer),
    repository: SentimentAnalysisRepository = Depends(get_sentiment_analysis_repository)
) -> SentimentService:
    """Get SentimentService instance with dependencies."""
    return SentimentService(
        feddit_client=feddit_client,
        sentiment_analyzer=sentiment_analyzer,
        repository=repository
    ) 