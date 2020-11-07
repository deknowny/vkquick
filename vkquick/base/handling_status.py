import typing as ty

import pydantic

from vkquick.base.filter import Decision


class HandlingStatus(pydantic.BaseModel):
    """
    Схема отчета от `EventHandler` по обработке события
    """

    reaction_name: str

    all_filters_passed: bool
    """
    Все ли фильтры пройдены
    """

    taken_time: float
    """
    Время, затраченное на обработку реакции (включая фильтры и подготовку аргументов)
    """

    filters_response: ty.List[ty.Tuple[str, Decision]] = pydantic.Field(
        default_factory=list
    )
    """
    Для каждого элемента списка:
    * Событие прошло/не прошло
    * Описание решения фильтра (причина обработки/не обработки) 
    * Имя фильтра (`__name__` атрибут)
    """

    passed_arguments: ty.Dict[str, ty.Any] = pydantic.Field(
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
