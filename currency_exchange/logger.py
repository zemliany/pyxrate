# fmt: off

import logging
from enum import Enum


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    NOTSET = logging.NOTSET


class LoggerConfig:
    def __init__(self, name: str = __name__, level: LogLevel = LogLevel.NOTSET):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level.value)
        self._configure_handler()

    def _configure_handler(self):
        if not self.logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def get_logger(self) -> logging.Logger:
        return self.logger

    @property
    def log_level(self) -> LogLevel:
        return self._log_level

    @log_level.setter
    def log_level(self, level: LogLevel | str):
        """Set the log level dynamically using LogLevel Enum or a string."""

        if isinstance(level, str):
            try:
                level = LogLevel[level.upper()]
            except KeyError:
                raise ValueError(f"Invalid log level: {level}. Must be one of: {', '.join(LogLevel.__members__.keys())}") # noqa
        elif not isinstance(level, LogLevel):
            raise ValueError(f"Log level must be a LogLevel Enum or a valid string. Received: {level}")

        self.logger.setLevel(level.value)
        self.logger.info(f"Log level set to {level.name}")
