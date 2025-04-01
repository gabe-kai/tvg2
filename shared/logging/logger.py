# shared/logging/logger.py

"""
Logger interface for TheVassalGame.
Use get_logger(__name__) in any module to retrieve a configured namespaced logger.
"""

import logging
from shared.logging import log_config

_initialized = False

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger configured with namespace `name`.
    Ensures logging is configured exactly once.
    """
    global _initialized
    if not _initialized:
        log_config.configure_logging()
        _initialized = True

    return logging.getLogger(name)
