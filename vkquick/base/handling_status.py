import dataclasses
import typing as ty

from vkquick.base.filter import Decision

if ty.TYPE_CHECKING:  # pragma: no cover
    from vkquick.context import Context


@dataclasses.dataclass
class HandlingStatus:
    """
    Схема отчета от `EventHandler` по обработке события
    """

    reaction_name: str
    """
    Имя реакции (обработчика)
    """

    all_filters_passed: bool
    """
    Все ли фильтры пройдены
    """

    taken_time: float
    """
    Время, затраченное на обработку реакции (включая фильтры и подготовку аргументов)
    """

    context: "Context"
    """
    Контекст, используемый командой. Сделано для удобного получения при использовании вейтеров
    """

    filters_response: ty.List[ty.Tuple[str, Decision]] = dataclasses.field(
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
