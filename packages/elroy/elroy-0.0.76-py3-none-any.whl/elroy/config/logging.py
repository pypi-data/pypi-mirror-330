import logging
import os
from logging.handlers import RotatingFileHandler

import litellm

from .paths import get_log_file_path


def setup_logging():
    log_file_path = get_log_file_path()
    # Create the directory for the log file if it doesn't exist
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Remove all existing handlers from the root logger
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Configure the root logger
    file_handler = RotatingFileHandler(log_file_path, maxBytes=10 * 1024 * 1024, backupCount=5)  # 10MB
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[file_handler],  # 10MB
    )

    # Silence some noisy loggers
    for name in ["openai", "httpx", "litellm"]:
        logging.getLogger(name).setLevel(logging.WARNING)

    # Disable liteLLM's default logging
    litellm.set_verbose = False  # type: ignore # noqa F841
    litellm.suppress_debug_info = True  # noqa F841

    # Silence liteLLM's verbose logger
    litellm.verbose_logger.setLevel(logging.INFO)  # type: ignore
    for handler in litellm.verbose_logger.handlers[:]:  # type: ignore
        litellm.verbose_logger.removeHandler(handler)  # type: ignore
        litellm.verbose_logger.addHandler(file_handler)  # type: ignore

    # Disable propagation to the root logger for all loggers
    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).propagate = False
