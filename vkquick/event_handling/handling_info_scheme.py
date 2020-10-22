import typing as ty


class HandlingInfoScheme(ty.TypedDict):
    """
    Схема отчета от `EventHandler` по обработке события
    """

    handler: "vkquick.event_handling.event_handler.EventHandler"
    """
    Обработчик события
    """

    is_correct_event_type: bool
    """
    Корректен ли тип события
    """

    are_filters_passed: bool
    """
    Все ли фильтры пройдены
    """

    filters_decision: ty.List[ty.Tuple[bool, str, str]]
    """
    Для каждого элемента списка:
    * Событие прошло/не прошло
    * Описание решения фильтра (причина обработки/не обработки) 
    * Имя фильтра (`__name__` атрибут)
    """

    passed_arguments: ty.Dict[str, ty.Any]
    """
    Словарь переданных аргументов в саму функцию обработки
    (под ключом имя аргумента, под значение само значение аргумента).
    В случае отсутствия аргументов или какой-либо
    фильтр не пройден список передается пустой
    """

    taken_time: float
    """
    Затраченное время на обработку события
    """
