import abc
import typing as ty

from vkquick.current import fetch
from vkquick.context import Context


class UnmatchedArgument:
    """
    Пустышка для значения аргумента, не прошедшего матчинг
    """


class TextCutter(abc.ABC):

    api = fetch("api_invalid_argument", "api")

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

    async def invalid_value(
        self, argument_position: int, seems_missing: bool, context: Context,
    ) -> None:
        """
        Дефолтный текст для некорректных аргументов
        """
        seems_missing_text = ""
        if seems_missing:
            seems_missing_text = (
                "Вероятно, при вызове команды был пропущен аргумент."
            )

        extra_info = self.usage_description()
        if extra_info:
            extra_info = f"💡 {extra_info}"
        response = (
            f"💥 Команда вызвана с некорректным "
            f"по значению аргументом №[id0|{argument_position}]."
            f" {seems_missing_text}\n\n{extra_info} "
        )
        await context.msg.reply(response, disable_mentions=True)

    @staticmethod
    def usage_description() -> str:
        return ""
