import logging
import os
import tempfile
import time
from logging.handlers import RotatingFileHandler

from pydantic import BaseModel, Field

# from qt_logging.dockable_logger import ConsoleFormatter, LogHandler


class FileLogger:
    class Config(BaseModel):
        log_directory: str | None = Field(
            default=None, description="The directory to store the log files, if None a temporary directory will be used"
        )
        name: str = "python_log"
        max_size_kb: int = Field(default=5, description="The maximum size of the log file in KB")
        backup_count: int = Field(default=30, description="The number of backup log files to keep")

    config: Config

    def __init__(self, config: Config | None = None, font=None):
        if config is None:
            config = self.Config()

        self.config = config

        self.log = logging.getLogger(f"file logger {self.config.name}")

        # Configure the text edit
        self.log_directory = self.config.log_directory

        if self.log_directory is None:
            self.log_directory = tempfile.mkdtemp()

        # create a rotating log file handler
        filename = f"{self.config.name}_{time.strftime('%Y%m%d-%H%M%S')}.log"
        self.log_file_handler = RotatingFileHandler(
            filename=os.path.join(self.log_directory, filename),
            maxBytes=self.config.max_size_kb * 1024,
            backupCount=self.config.backup_count,
        )

        self.log_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.log_file_handler.setLevel(logging.DEBUG)

        self.log.info(f"Logging to file: {os.path.join(self.log_directory, filename)}")

    def register_logger(self, logger: logging.Logger):
        logger.addHandler(self.log_file_handler)
