import abc
import typing as ty

import vkquick.event_handling.reaction_argument.base
import vkquick.events_generators.event
import vkquick.event_handling.message


class UnmatchedArgument:
    """
    Пустышка для значения аргумента, не прошедшего матчинг
    """


class TextArgument(
    vkquick.event_handling.reaction_argument.base.ReactionArgument, abc.ABC
):
    @abc.abstractmethod
    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        """
        "Отрезает" аргумент с начала строки `arguments_string`,
        если его можно достать.

        Возвращает кортеж из:
        * Вытащенного значения аргумента текстовой команды. Если аргумент
        вытащить нельзя, первым значением кортежа возвращается `UnmatchedArgument`
        * Оставшаяся строка. Если аргумент не прошел, вернуть переданную строку
        """

    @staticmethod
    def cut_part_lite(
        regex: ty.Pattern,
        arguments_string: str,
        factory: ty.Callable[[ty.Match], ty.Any] = lambda match: match,
    ) -> ty.Tuple[ty.Any, str]:
        """
        Инкапсулирует логику, часто применяющуюся к `cut_part`
        """
        matched = regex.match(arguments_string)
        if matched:
            new_arguments_string = arguments_string[matched.end() :]
            return factory(matched), new_arguments_string

        return UnmatchedArgument, arguments_string

    def invalid_value(
        self,
        argument_name: str,
        argument_position: int,
        argument_string: str,
        event: vkquick.events_generators.event.Event,
    ) -> str:
        """
        Дефолтный текст для некорректных аргументов
        """
        seems_missing = ""
        if not argument_string:
            seems_missing = (
                "Вероятно, при вызове команды был пропущен аргумент."
            )

        extra_info = self.usage_description()
        if extra_info:
            extra_info = f"💡 {extra_info}"

        response = (
            f"💥 Во время обработки команды `[id0|{event.get_message_object().text}]` "
            "возникли технические шоколадки!\n\n"
            f"При попытке достать аргумент №[id0|{argument_position}]"
            f" ({argument_name}) полученно некорректное значение "
            f"`{argument_string}`. {seems_missing}\n\n"
            f"{extra_info}"
        )
        return response

    @staticmethod
    def usage_description() -> str:
        return ""
