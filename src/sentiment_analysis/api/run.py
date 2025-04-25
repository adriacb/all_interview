"""Run the FastAPI application."""

import uvicorn
from sentiment_analysis.api.main import app


if __name__ == "__main__":
    uvicorn.run(
        "sentiment_analysis.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 