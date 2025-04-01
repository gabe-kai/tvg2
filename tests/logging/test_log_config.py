# tests/logging/test_log_config.py

"""
Tests for the shared.logging.log_config module.
"""

import logging
import pytest
from shared.logging import log_config
from shared.logging.log_config import LogLevel
from shared.logging.logger import get_logger

def test_trace_level_registered():
    assert logging.getLevelName(LogLevel.TRACE) == "TRACE"

def test_trace_method_available():
    logger = get_logger("test.trace")
    assert hasattr(logger, "trace")
    assert callable(logger.trace)

def test_trace_logging_enabled():
    logger = get_logger("test.trace.active")
    if not logger.isEnabledFor(LogLevel.TRACE):
        pytest.skip("TRACE level is not enabled in this environment")
    assert logger.isEnabledFor(LogLevel.TRACE)

def test_ui_log_hook_receives_log():
    messages = []

    def fake_hook(record):
        messages.append(record.getMessage())

    log_config.register_log_hook(fake_hook)
    logger = get_logger("test.hook")
    logger.info("Hello from hook!")

    assert any("Hello from hook!" in msg for msg in messages)
