import logging
from os import path
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler


ROOT_PATH = path.abspath(path.join(path.dirname(__file__), "..", "..", ".."))
LOG_PATH = path.join(ROOT_PATH, "logs")
LOG_FILENAME = "state-consumption.log"
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
FORMATTER = logging.Formatter(LOG_FORMAT, DATE_FORMAT)


class LogHandler:
    """A handler for all log system operations."""

    _file_handler: TimedRotatingFileHandler
    logger: logging.Logger

    def __init__(self) -> None:
        try:
            folder_exist = self.create_file()
            if not folder_exist:
                return
            self._file_handler = TimedRotatingFileHandler(
                f"{LOG_PATH}/{LOG_FILENAME}",
                when="W0",
                interval=1,
                backupCount=4,
                encoding="utf-8",
                utc=True,
            )
            self._file_handler.setFormatter(FORMATTER)
            logging.basicConfig(
                level=logging.INFO,
                handlers=[self._file_handler],
            )
            self.logger = logging.getLogger(__name__)
        except Exception as e:
            print(f"Log Error - {e}")

    def create_file(self) -> bool:
        """Create file to save logs."""
        try:
            path = Path(LOG_PATH)
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(e)
            return False


logHandler = LogHandler()
logger = logHandler.logger


if __name__ == "__main__":
    print(ROOT_PATH)
    logHandler.create_file()
    logger.info("Testing logging!")
