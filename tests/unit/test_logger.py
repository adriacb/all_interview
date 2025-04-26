"""Unit tests for the logger configuration."""

import logging
from unittest.mock import patch, MagicMock
import structlog

from sentiment_analysis.logger import configure_logger


def test_configure_logger_returns_bound_logger():
    """Test that configure_logger returns a BoundLogger instance."""
    with patch("structlog.get_logger") as mock_get_logger:
        mock_logger = MagicMock(spec=structlog.BoundLogger)
        mock_get_logger.return_value = mock_logger
        logger = configure_logger()
        assert isinstance(logger, structlog.BoundLogger)


def test_configure_logger_sets_up_structlog():
    """Test that structlog is configured correctly."""
    with patch("structlog.configure") as mock_configure:
        configure_logger()
        mock_configure.assert_called_once()
        call_args = mock_configure.call_args[1]
        
        # Check processors
        processors = call_args["processors"]
        assert any(isinstance(p, structlog.processors.TimeStamper) for p in processors)
        assert any(p == structlog.processors.add_log_level for p in processors)
        assert any(isinstance(p, structlog.processors.StackInfoRenderer) for p in processors)
        
        # Check other configurations
        assert call_args["wrapper_class"] == structlog.BoundLogger
        assert call_args["context_class"] == dict
        assert isinstance(call_args["logger_factory"], type(structlog.PrintLoggerFactory()))
        assert not call_args["cache_logger_on_first_use"]


def test_configure_logger_sets_up_standard_logging():
    """Test that standard logging is configured correctly."""
    with patch("logging.basicConfig") as mock_basic_config:
        configure_logger()
        mock_basic_config.assert_called_once()
        call_args = mock_basic_config.call_args[1]
        
        assert call_args["format"] == "%(message)s"
        assert call_args["level"] == logging.INFO
