"""
Основоположник всех аннотационных типов
"""
from abc import abstractmethod, ABC


class Annotype(ABC):
    """
    Позволяет создавать свои аннотационные типы
    """

    @abstractmethod
    def prepare(
        self,
        argname: str,
        event: "vkquick.annotypes.event.Event",
        func: "vkquick.reaction.Reaction",
        bin_stack: type,
    ):
        """
        Вызывается перед тем,
        как аргументы попадут в код команды.
        Метод должен вернуть значение для аргумента

        ## Параметры:
        * `argname`: Имя аргумента, на который будет вызван код команды
        * `event`: Событие LongPoll
        * `com`: Объект команды
        * `bin_stack`: Поле, присутствующее только среди
        проверки одной реакции на валидность и подготовки аргументов.
        Помогает избегать гонку данных. Своего рода payload
        """
