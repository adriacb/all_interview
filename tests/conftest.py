"""Test configuration and fixtures."""

import os
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock environment variables for tests."""
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-api-key",
        "FEDDIT_API_URL": "http://test-feddit:8080",
        "FAST_API_PORT": "8000",
        "PRODUCTION": "true"  # Prevent loading from .env file
    }):
        yield
