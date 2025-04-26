"""Configuration module for the sentiment analysis service."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Get the root directory (where .env is located)
ROOT_DIR = Path(__file__).parent.parent.parent

# Load environment variables from .env file in root directory if not in production
if not os.getenv("PRODUCTION"):
    load_dotenv(dotenv_path=ROOT_DIR / ".env")

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FAST_API_PORT = int(os.getenv("FAST_API_PORT", "8000"))
FEDDIT_API_URL = os.getenv("FEDDIT_API_URL", "http://localhost:8080")

# Validate required environment variables
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")
