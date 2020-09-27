import typing as ty


class HandlingInfo(ty.TypedDict):
    """
    Схема, возвращаемая после вызова `handle_event`
    у обертки обработчика
    """

    handler_decision: ty.Tuple[bool, str]
    """
    Решение самого обработчика: прошел/не прошел, причина
    """

    arguments: ty.Dict[str, ty.Any]
    """
    Переданные аргументы в функцию обработчика
    (если таковы имеются)
    """

    filters_state: ty.Dict[str, ty.Tuple[bool, str]]
    """
    Состояние фильтров. Имя фильтра: Прошел/не прошел, причина
    """
