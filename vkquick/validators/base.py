"""
Структура любого валидатора
"""
from abc import abstractmethod, ABC

from vkquick.annotypes.event import Event
import typing


class Validator(ABC):
    """
    Базовый класс для всех валидаторов
    (Дектораторов над реакциями)
    """

    def __call__(self, func):
        """
        Вызывается по время декорирования
        """
        if hasattr(func, "validators"):
            func.validators.append(self)
        return func

    @abstractmethod
    def validate(self, event: Event) -> None:
        """
        Определяет, валидна ли команда (reaction) или нет.
        Возбуждает исключение в случае ошибки.

        ## Параметры
        * `event`: Событие LongPoll
        """
        pass

    def collect(self) -> typing.Optional[dict]:
        return None
