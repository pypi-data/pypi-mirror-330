import logging

from pathlib import Path
from typing import ClassVar


DEFAULT_NAME = "hyLog"

class AppConfig:
    name: str = DEFAULT_NAME
    output_dir: Path | None = None
    initialized: bool = False
    seen_names: ClassVar[set[str]] = set(DEFAULT_NAME)

class FileConfig:
    level: int = logging.DEBUG
    max_bytes: int = 3_000_000
    backup_count: int = 3
    mode = "w"
    rotating_suffix = "_rotating.log"
    last_suffix = "_last.log"
    json_suffix = "_json.jsonl"

class StreamConfig:
    level: int = logging.WARNING

class Config:
    file: FileConfig = FileConfig()
    stream: StreamConfig = StreamConfig()
    app: AppConfig = AppConfig()
