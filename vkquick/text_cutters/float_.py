"""
Float аргумент
"""
import re
import typing as ty

from vkquick.base.text_cutter import TextCutter, UnmatchedArgument


class Float(TextCutter):
    """
    Дробное число
    """

    def __init__(
        self,
        *,
        min_: int = None,
        max_: int = None,
    ) -> None:
        if isinstance(min_, int) and isinstance(max_, int) and min_ > max_:
            raise ValueError("max_ can't be less than min_")
        self.min_ = min_
        self.max_ = max_
        self.pattern = re.compile(r"-?\d*(?:\.\d+)?")

    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        value, parsed_string = self.cut_part_lite(
            self.pattern, arguments_string, lambda x: float(x.group(0)),
        )
        if (
            value is not UnmatchedArgument
            and (self.min_ is None or value >= self.min_)
            and (self.max_ is None or value <= self.max_)
        ):
            return value, parsed_string

        return UnmatchedArgument, parsed_string

    def usage_description(self):
        description = "Аргумент должен быть десятичной дробью."
        if self.min_ is not None:
            description += f" Минимальное значение {self.min_}."
        if self.max_ is not None:
            description += f" Максимальное значение {self.max_}."
        return description
