import atexit
import logging.handlers
import sys

from multiprocessing import Queue
from pathlib import Path

from hylog import config
from hylog import formatters


Config = config.Config()

# File handlers
def _format_output_file_path(*args, **kwargs) -> tuple[Path, str]:
    """Retrieve and validate that the user passed a name and output directory.

    Returns the path to the output file.
    """
    output_dir = kwargs.get("output_dir")
    name = kwargs.get("name")

    if output_dir is None or name is None:
        raise ValueError(
            f"output_dir and name must be provided. Got {output_dir=} and {name=}"
        )

    if not Path(output_dir).is_dir():
        raise FileNotFoundError(f"Output directory {output_dir} does not exist.")

    return Path(output_dir), name

class FileLastRun(logging.FileHandler):
    _formatter: logging.Formatter = formatters.Detailed()
    _mode: str = "w"

    def __init__(self, *args, **kwargs) -> None:
        """
        Logs the last run of the application to a file.

        The file is overwritten each time the application is run.
        """
        output_dir, name = _format_output_file_path(*args, **kwargs)
        file_path = output_dir / (name + Config.file.last_suffix)

        super().__init__(file_path, mode=self._mode)

        self.setLevel(Config.file.level)
        self.setFormatter(self._formatter)


class FileRotating(logging.handlers.RotatingFileHandler):
    _formatter: logging.Formatter = formatters.Detailed()
    # _level: int = logging.DEBUG
    # _suffix = "_rotating.log"

    _max_bytes: int = 3_000_000
    _backup_count: int = 3

    def __init__(self, *args, **kwargs) -> None:
        output_dir, name = _format_output_file_path(*args, **kwargs)
        file_path = output_dir / (name + Config.file.rotating_suffix)

        super().__init__(
            file_path, maxBytes=self._max_bytes, backupCount=self._backup_count
        )

        self.setLevel(Config.file.level)
        self.setFormatter(self._formatter)


class JSONHandler(logging.handlers.RotatingFileHandler):
    _formatter: logging.Formatter = formatters.JSON()

    def __init__(self, *args, **kwargs) -> None:
        output_dir, name = _format_output_file_path(*args, **kwargs)
        file_path = output_dir / (name + Config.file.json_suffix)

        super().__init__(
            file_path, maxBytes=Config.file.max_bytes, backupCount=Config.file.backup_count
        )

        self.setLevel(Config.file.level)
        self.setFormatter(self._formatter)


# Stream handlers
class StandardOutput(logging.StreamHandler):
    _formatter: logging.Formatter = formatters.Simple()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(stream=sys.stdout)
        user_level = kwargs.get("stdout_level")
        if user_level is not None:
            _stdout_level = getattr(logging, user_level.upper())
        else:
            _stdout_level = Config.stream.level

        self.setLevel(_stdout_level)
        self.setFormatter(self._formatter)


# Queue handlers
class QueueHandler(logging.handlers.QueueHandler):
    def __init__(self, queue: Queue) -> None:
        super().__init__(queue)


class QueueListener(logging.handlers.QueueListener):
    def __init__(self, queue, *handlers: logging.Handler) -> None:
        super().__init__(queue, *handlers, respect_handler_level=True)


def setup_handlers(*args, **kwargs) -> None:
    """Instantiae and add all handlers to the QueueListener/Handler and configure logger."""
    name = kwargs.get("name", "default_logger")
    if name is None:
        raise ValueError("Logger name must be provided")

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    log_queue = Queue(-1)
    queue_handler = QueueHandler(log_queue)

    logger.addHandler(queue_handler)

    handler_classes = [
        StandardOutput,
        FileLastRun,
        FileRotating,
        JSONHandler,
    ]

    queue_listener = QueueListener(
        log_queue,
        *[handler(*args, **kwargs) for handler in handler_classes],
    )

    queue_listener.start()
    atexit.register(queue_listener.stop)
