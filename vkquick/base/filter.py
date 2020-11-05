import abc
import dataclasses
import enum
import typing as ty

import vkquick.utils

# import vkquick.context


class Decision(ty.NamedTuple):
    passed: bool
    description: str


class Filter(abc.ABC):
    """
    Фильтр говорит сам за себя -- он фильтрует
    событие по каким-либо параметрам внутри.
    Помещать фильтр нужно над декоратором обработки реакции.
    После обработки события (методом `make_decision`)
    возвращает специальный объект `FilterResponse`.

    В `Command` статус обработки фильтра может быть использован,
    чтобы задать отдельную реакцию. (Например, нужно, чтобы
    пользователь отправил фотографию. Вы можете быстро
    определить поведение, когда фотография не отправлена)
    """

    @abc.abstractmethod
    def make_decision(self, context: "vkquick.context.Context") -> Decision:
        """
        Определяет, подходит ли событие по критериям фильтра
        """

    def __call__(self, command: "vkquick.command.Command") -> ty.Any:
        """
        Вызывается в момент декорирования.
        Фильтры должны быть указаны над хендлером событий
        """
        command.filters.append(self)
        return command
