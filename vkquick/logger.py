import sys

from loguru import logger

logger.remove(0)


class LoggingLevel:
    def __init__(self, level):
        self.level = level

    def __call__(self, record):
        level_no = logger.level(self.level).no
        return record["level"].no >= level_no


def update_logging_level(level):
    level_handler.level = level


level_handler = LoggingLevel("INFO")
logger_handler = logger.add(
    sys.stdout,
    format=(
        "<lvl><n>["
        "{level.name[0]} "
        "</n></lvl><c>{time:YYYY-MM-DD HH:mm:ss.SSS}</c><lvl><n>"
        "]</n></lvl>"
        ": <lvl><n>{message}</n></lvl>"
    ),
    filter=level_handler,
    level=0,
)
