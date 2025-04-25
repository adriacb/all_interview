"""API package for the sentiment analysis microservice.

This package contains the FastAPI application and all HTTP-related components.
The API layer is kept thin and delegates business logic to the application layer.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sentiment_analysis.api.routes import router
from sentiment_analysis.api.dependencies import get_sentiment_service
from sentiment_analysis.logger import configure_logger


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    app = FastAPI(
        title="Sentiment Analysis API",
        description="API for analyzing sentiment of Feddit comments",
        version="1.0.0"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Configure logging
    logger = configure_logger().bind(service="api")
    logger.info("Starting Sentiment Analysis API")
    
    # Include routes
    app.include_router(router)
    
    return app 