"""
Integer аргумент
"""
import re
import typing as ty

import vkquick.base.text_argument


class Integer(vkquick.base.text_argument.TextArgument):
    """
    Целое число
    """

    def __init__(
        self, *, only_decimal: bool = False, range_: ty.Optional[range] = None
    ):
        self.only_decimal = only_decimal  # TODO
        self.range_ = range_
        self.pattern = re.compile(r"\d+")

    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        value, parsed_string = self.cut_part_lite(
            self.pattern, arguments_string, lambda x: int(x.group(0)),
        )
        if (
            value is not vkquick.base.text_argument.UnmatchedArgument
            and self.range_ is not None
            and value not in self.range_
        ):
            return (
                vkquick.base.text_argument.UnmatchedArgument,
                arguments_string,
            )

        return value, parsed_string

    def usage_description(self):
        description = "Аргумент должен быть целым числом."
        if self.range_ is not None:
            range_info = f" Число должно быть ≥ {self.range_.start}, ≤ {self.range_.stop - 1}"
            if self.range_.step == 1:
                range_info += "."
            else:
                range_info += f" с шагом {self.range_.step}."
            description += range_info
        return description
