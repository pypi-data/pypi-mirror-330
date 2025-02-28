import logging.config
import logging.handlers

from pathlib import Path
from typing import cast

from hylog import config
from hylog import handlers
from hylog import logger


Config = config.Config()


def get_app_logger(
    app_name: str,
    output_dir: str | Path,
    stdout_level: str | None = None,
) -> logger._AppLogger:
    """Create a logger for the application with the given name and output directory."""
    # TODO: Add support for showing path to module rather than just the name?
    # TODO: Add support to disable file logging
    Config.app.name = app_name
    Config.app.output_dir = Path(output_dir)

    logging.setLoggerClass(logger._AppLogger)

    # Configure all handlers and logging levels into a QueueHandler
    handlers.setup_handlers(
        output_dir=Path(output_dir), name=app_name, stdout_level=stdout_level
    )

    Config.app.initialized = True

    return cast(logger._AppLogger, logging.getLogger(app_name))

def get_logger(
    name: str | None = None,
) -> logger._AppLogger:
    """Create a logger for the application with the given name and output directory."""
    if not Config.app.initialized:
        raise RuntimeError("App logger must be initialized before creating a logger")

    elif name == Config.app.name or name is None:
        return cast(logger._AppLogger ,logging.getLogger(Config.app.name))
    else:
        return cast(logger._AppLogger ,logging.getLogger(Config.app.name).getChild(name))