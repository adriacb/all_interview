"""FastAPI application for sentiment analysis."""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sentiment_analysis.api.routes import router
from sentiment_analysis.api.dto import SentimentAnalysisResponseDTO
from sentiment_analysis.logger import configure_logger
from sentiment_analysis.config import FAST_API_PORT

logger = configure_logger().bind(service="api")

app = FastAPI(
    title="Sentiment Analysis API",
    description="API for analyzing sentiment of Feddit comments",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=FAST_API_PORT, reload=True) 