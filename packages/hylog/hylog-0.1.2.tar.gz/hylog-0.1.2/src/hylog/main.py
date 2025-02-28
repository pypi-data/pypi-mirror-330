import atexit
import logging.config
import logging.handlers

from pathlib import Path

from hylog import handlers
from hylog import logger


def get_app_logger(
    name: str,
    output_dir: str | Path,
    stdout_level: str | None = None,
) -> logger._AppLogger:
    """Create a logger for the application with the given name and output directory."""
    logging.setLoggerClass(logger._AppLogger)

    # Configure all handlers and logging levels into a QueueHandler
    handlers.setup_handlers(
        output_dir=Path(output_dir), name=name, stdout_level=stdout_level
    )

    return logging.getLogger(name) # type: ignore
