"""
Структура любого валидатора
"""
from abc import abstractmethod, ABC

from vkquick.annotypes.event import Event
from vkquick.reaction import Reaction


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
    def isvalid(self, event: Event, com: Reaction, bin_stack: type):
        """
        Определяет, валидна ли команда (reaction) или нет.
        Возвращает кортеж из 2х элементов:

        1. Валидна/нет (True/False). Если хотя бы один
        валидатор команды не валиден, команда не вызывается
        1. Сообщение (для False), указывающее причину,
        по которой команда не валидна.
        Используется в режиме дебага (флаг `-d`)

        ## Параметры
        * `event`: Событие LongPoll
        * `com`: Объект команды
        * `bin_stack`: Поле, присутствующее только среди
        проверки одной реакции на валидность и подготовки аргументов.
        Помогает избегать гонку данных. Своего рода payload
        """
