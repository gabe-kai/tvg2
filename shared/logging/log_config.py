# shared/logging/log_config.py

import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from typing import Callable, List

# === Centralized Log Levels ===
class LogLevel:
    TRACE = 5
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

logging.addLevelName(LogLevel.TRACE, "TRACE")

def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(LogLevel.TRACE):
        self._log(LogLevel.TRACE, message, args, **kwargs)

logging.Logger.trace = trace  # Monkeypatch trace() into logger


# === Formatters ===
class LogFormat:
    SIMPLE = "[%(levelname)s] %(message)s"
    DETAILED = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    FILE = "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s"


# === Console Formatter with Color Support ===
class ColoredFormatter(logging.Formatter):
    COLORS = {
        "TRACE": "\033[94m",   # Bright Blue
        "DEBUG": "\033[36m",   # Cyan
        "INFO": "\033[32m",    # Green
        "WARNING": "\033[33m", # Yellow
        "ERROR": "\033[31m",   # Red
        "CRITICAL": "\033[1;31m" # Bold Red
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"


# === UI Hook Forwarding ===
_log_hooks: List[Callable[[logging.LogRecord], None]] = []

class ForwardingHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        for hook in _log_hooks:
            try:
                hook(record)
            except Exception:
                pass  # Prevent hook failures from crashing logging

def register_log_hook(hook_fn: Callable[[logging.LogRecord], None]):
    if hook_fn not in _log_hooks:
        _log_hooks.append(hook_fn)


# === Handler Factories ===
def create_console_handler():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(LogLevel.DEBUG)
    formatter = ColoredFormatter(LogFormat.DETAILED)
    handler.setFormatter(formatter)
    return handler

def create_file_handler(log_dir="logs", filename="vassal.log"):
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(log_dir, filename)
    handler = RotatingFileHandler(
        path,
        maxBytes=5 * 1024 * 1024,
        backupCount=9,
        encoding="utf-8"  # Ensure Unicode support in log files
    )
    handler.setLevel(LogLevel.DEBUG)
    formatter = logging.Formatter(LogFormat.FILE)
    handler.setFormatter(formatter)
    return handler

def create_forwarding_handler():
    handler = ForwardingHandler()
    handler.setLevel(LogLevel.DEBUG)
    return handler


# === Logging Configuration Entrypoint ===
def configure_logging(env="development"):
    root = logging.getLogger()
    if getattr(configure_logging, "_configured", False):
        return  # Prevent duplicate configuration

    root.setLevel(LogLevel.DEBUG if env == "development" else LogLevel.INFO)
    root.addHandler(create_console_handler())
    root.addHandler(create_file_handler())
    root.addHandler(create_forwarding_handler())

    configure_logging._configured = True
