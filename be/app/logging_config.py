import logging
import logging.config
from typing import Any, Dict

from app.config import settings


LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        },
        "uvicorn": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "uvicorn": {
            "class": "logging.StreamHandler",
            "formatter": "uvicorn",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["uvicorn"],
            "level": settings.log_level,
            "propagate": False,
        },
        "uvicorn.error": {
            "level": settings.log_level,
        },
        "uvicorn.access": {
            "handlers": ["uvicorn"],
            "level": settings.log_level,
            "propagate": False,
        },
        "app": {
            "handlers": ["console"],
            "level": settings.log_level,
            "propagate": False,
        },
    },
}


def setup_logging() -> None:
    """配置 logging."""
    logging.config.dictConfig(LOGGING_CONFIG)
