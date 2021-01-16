import abc
import dataclasses
import typing as ty

from vkquick.context import Context


class UnmatchedArgument:
    """
    Пустышка для значения аргумента, не прошедшего матчинг
    """


@dataclasses.dataclass
class AdvancedArgumentDescription:

    cutter_description: ty.Union[str, ty.Callable[[Context, int, int], str]]

    def build_explanation(
        self, context, argument_position: int, seems_missing: bool
    ):
        seems_missing_text = ""
        if seems_missing:
            seems_missing_text = (
                "Вероятно, при вызове команды был пропущен аргумент."
            )
        if callable(self.cutter_description):
            extra_info = self.cutter_description(
                context, argument_position, seems_missing
            )
        else:
            extra_info = self.cutter_description
        if extra_info:
            extra_info = f"💡 {extra_info}"
        response = (
            f"⚠ Команда вызвана с некорректным "
            f"по значению аргументом №[id0|{argument_position}]."
            f" {seems_missing_text}\n{extra_info} "
        )
        return response


class TextCutter(abc.ABC):
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

    def invalid_value_text(
        self, context, argument_position: int, seems_missing: bool
    ) -> str:
        """
        Дефолтный текст для некорректных аргументов
        """
        text_builder = AdvancedArgumentDescription(self.usage_description())
        return text_builder.build_explanation(
            context, argument_position, seems_missing
        )

    @staticmethod
    def usage_description() -> str:
        return ""  # pragma: no cover
