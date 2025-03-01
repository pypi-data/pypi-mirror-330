#!/usr/bin/env python3

import logging
import os
from logging.handlers import RotatingFileHandler

"""
Handles logging for REDCap-EDA with log rotation and dynamic log levels.
- each log file will not exceed 1MB
- Keeps the last 5 log files (redcap_eda.log.1, redcap_eda.log.2, etc.).
- Older logs are automatically deleted after the 6th file.
"""

# Define log directory and file
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
LOG_FILE = os.path.join(LOG_DIR, "redcap_eda.log")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Create a RotatingFileHandler (max 1MB per file, keep last 5)
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=5)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"),
)

# Create logger instance
logger = logging.getLogger("REDCap-EDA")
logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())

# Default log level (INFO)
logger.setLevel(logging.INFO)


def set_log_level(debug_mode=False):
    """
    Dynamically set the logging level.

    Args:
        debug_mode (bool): If True, set logging to DEBUG. Otherwise, keep INFO.
    """
    new_level = logging.DEBUG if debug_mode else logging.INFO
    logger.setLevel(new_level)
    logger.info(f"Logging level set to {'DEBUG' if debug_mode else 'INFO'}")
