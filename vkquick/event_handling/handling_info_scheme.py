import dataclasses
import typing as ty


# pydantic?
@dataclasses.dataclass
class HandlingInfoScheme:
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

    all_filters_passed: bool
    """
    Все ли фильтры пройдены
    """

    taken_time: float
    """
    Время, затраченное на обработку реакции (включая фильтры и подготовку аргументов)
    """

    filters_decision: ty.List[ty.Tuple[bool, str, str]] = dataclasses.field(
        default_factory=list
    )
    """
    Для каждого элемента списка:
    * Событие прошло/не прошло
    * Описание решения фильтра (причина обработки/не обработки) 
    * Имя фильтра (`__name__` атрибут)
    """

    passed_arguments: ty.Dict[str, ty.Any] = dataclasses.field(
        default_factory=dict
    )
    """
    Словарь переданных аргументов в саму функцию обработки
    (под ключом имя аргумента, под значение само значение аргумента).
    В случае отсутствия аргументов или какой-либо
    фильтр не пройден список передается пустой
    """

    exception_text: str = ""
    """
    Если реакция подняла исключение, то его текст отобразится
    """
