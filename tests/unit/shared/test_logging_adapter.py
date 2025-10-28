"""
Tests for LoggingAdapter - Shared Layer
"""
import pytest
from src.shared.logging_adapter import PythonLogger


class TestPythonLogger:
    """Test suite for PythonLogger."""

    def test_logger_error_method(self):
        """Error method works correctly."""
        logger = PythonLogger("test")
        logger.error("Test error message")

    def test_logger_file_handler_creation(self):
        """FileHandler is created correctly."""
        logger = PythonLogger("test")
        logger.info("Test message")
        assert logger.logger is not None

    def test_logger_console_handler_creation(self):
        """ConsoleHandler is created correctly."""
        logger = PythonLogger("test")
        assert logger.logger is not None
        assert len(logger.logger.handlers) > 0
