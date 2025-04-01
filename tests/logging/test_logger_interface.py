# tests/logging/test_logger_interface.py

"""
Tests for the shared.logging.logger interface.
"""

import logging
from shared.logging.logger import get_logger

def test_get_logger_returns_logger():
    logger = get_logger("test.module")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test.module"

def get_effective_handlers(logger):
    while logger:
        if logger.handlers:
            return logger.handlers
        logger = logger.parent
    return []

def test_logger_includes_handlers():
    logger = get_logger("test.handlers")
    assert get_effective_handlers(logger), "Logger should inherit at least one handler"
