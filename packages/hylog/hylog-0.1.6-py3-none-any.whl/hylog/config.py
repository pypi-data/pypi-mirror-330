import logging

from pathlib import Path


class AppConfig:
    name: str | None = None
    output_dir: Path | None = None
    initialized: bool = False

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
