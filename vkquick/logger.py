import dataclasses
import sys

from loguru import logger


# Удаление настроек логгера по умолчанию
logger.remove(0)


@dataclasses.dataclass
class LoggingLevel:
    """
    Вспомогательный класс для фильтрации
    логов по их уровню
    """
    level: str

    def __call__(self, record: dict) -> bool:
        level_no = logger.level(self.level).no
        return record["level"].no >= level_no


def update_logging_level(level: str) -> None:
    """
    Обновляет уровень логов логгера

    Arguments:
        level: Новый уровень для логов
    """
    level_handler.level = level


# По умолчанию логгер выставлен в уровень INFO
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
