"""Dependency injection for the API layer."""

from fastapi import Depends
from typing import Annotated

from sentiment_analysis.application.services.sentiment_service import SentimentService
from sentiment_analysis.infrastructure.clients.feddit_client import FedditClient
from sentiment_analysis.infrastructure.sentiment_analyzer import SentimentAnalyzer
from sentiment_analysis.domain.repositories.sentiment_analysis_repository import SentimentAnalysisRepository
from sentiment_analysis.logger import configure_logger


def get_feddit_client() -> FedditClient:
    """Get FedditClient instance.
    
    Returns:
        FedditClient: Configured FedditClient instance.
    """
    return FedditClient()


def get_sentiment_analyzer() -> SentimentAnalyzer:
    """Get SentimentAnalyzer instance.
    
    Returns:
        SentimentAnalyzer: Configured SentimentAnalyzer instance.
    """
    return SentimentAnalyzer()


def get_sentiment_service(
    feddit_client: Annotated[FedditClient, Depends(get_feddit_client)],
    sentiment_analyzer: Annotated[SentimentAnalyzer, Depends(get_sentiment_analyzer)],
    repository: Annotated[SentimentAnalysisRepository, Depends(get_repository)]
) -> SentimentService:
    """Get SentimentService instance.
    
    Args:
        feddit_client: Injected FedditClient
        sentiment_analyzer: Injected SentimentAnalyzer
        repository: Injected SentimentAnalysisRepository
        
    Returns:
        SentimentService: Configured SentimentService instance.
    """
    return SentimentService(
        feddit_client=feddit_client,
        sentiment_analyzer=sentiment_analyzer,
        repository=repository
    ) 