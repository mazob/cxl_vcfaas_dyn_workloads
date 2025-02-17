"""Module with Python logging functionalities."""

import logging.config
import os
from datetime import datetime
from typing import Any, Optional


def config(prog_name: str, config: Optional[dict[str, Any]] = None) -> None:
    """Configure logging.

    Args:
        prog_name: program name, i.e. filename/module name.
        config: optional configuration for logging.
    """

    log_filename = "".join(
        [prog_name, "_", datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), ".log"]
    )
    log_file_path = os.path.join(os.path.dirname(__file__), "../logs", log_filename)

    default_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "style": "{",
                "format": "{asctime} - {levelname:<8s} - {name} - {lineno:>3d} - {message}",
            },
            "stream": {
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "style": "{",
                "format": "{message}",
            }
        },
        "handlers": {
            "stream": {
                "level": 'INFO',
                "formatter": "standard",
                "class": "logging.StreamHandler"            },
        },
        "loggers": {"root": {"level": "DEBUG", "handlers": ["stream"]}},
    }

    if not config:
        config = default_config

    logging.config.dictConfig(config)
