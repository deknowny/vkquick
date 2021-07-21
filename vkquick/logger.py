import dataclasses
import sys
import typing
import uuid

from loguru import logger

# Если есть логгер по умолчанию
try:
    logger.remove(0)
# Если такого нет
except ValueError:
    pass


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


class SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


def format_mapping(
    message: str,
    pair_spec: str,
    mapping: typing.Mapping,
    pair_join_string: str = ", ",
    mapping_reference_name: str = "params",
) -> dict:
    prepared_mapping = {}
    prepared_formatting_strings = []
    for key, value in mapping.items():
        key_formatting_name = uuid.uuid1().hex
        value_formatting_name = uuid.uuid1().hex
        prepared_mapping[key_formatting_name] = key
        prepared_mapping[value_formatting_name] = value
        prepared_formatting_strings.append(
            pair_spec.format(
                key=f"{{{key_formatting_name}}}",
                value=f"{{{value_formatting_name}}}",
            )
        )

    updated_mapping_param = SafeDict(
        {
            mapping_reference_name: pair_join_string.join(
                prepared_formatting_strings
            )
        }
    )
    return dict(
        # Logging message
        _Logger__message=message.format_map(updated_mapping_param),
        **prepared_mapping,
    )
