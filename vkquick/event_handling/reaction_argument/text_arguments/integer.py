import re
import typing as ty

from . import base
import vkquick.events_generators.event


class Integer(base.TextArgument):
    """
    Целое число.
    """

    always_be_instance = True

    def __init__(
        self, only_decimal: bool = False, range_: ty.Optional[range] = None
    ):
        self.only_decimal = only_decimal
        self.range_ = range_

    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        values = self.cut_part_lite(
            re.compile(r"(\d+[^oxb\s])"),
            arguments_string,
            lambda x: int(x.group(1)),
        )
        if values[0] is base.UnmatchedArgument and not self.only_decimal:
            values = (
                self._match_diff_notation(
                    ("x", "X"),
                    r"(0?(?:x|X)(?:\d|[a-fA-F])+)",
                    16,
                    arguments_string,
                )
                or self._match_diff_notation(
                    ("o", "O"), r"(0?(?:o|O\d+))", 8, arguments_string
                )
                or self._match_diff_notation(
                    ("b", "B"), r"(0?(?:b|B)\d+)", 2, arguments_string
                )
                or (base.UnmatchedArgument, arguments_string,)
            )
        if self.range_ is not None:
            if values[0] not in self.range_:
                return base.UnmatchedArgument, arguments_string
        return values

    @staticmethod
    def _match_diff_notation(
        starts: tuple, pattern: str, notation: int, arguments_string
    ):
        match_as_hex = re.match(pattern, arguments_string)
        if match_as_hex is not None:
            val = match_as_hex.group(1)
            if val.startswith(starts):
                val = "0" + val
            val = int(val, base=notation)
            return val, arguments_string[match_as_hex.end() :]

    def invalid_value(
        self,
        argument_name: str,
        argument_position: int,
        argument_string: str,
        event: vkquick.events_generators.event.Event,
    ) -> str:
        response = base.TextArgument.invalid_value(
            argument_name, argument_position, argument_string, event
        )
        return response + self.extra_invalid_value_info()

    def extra_invalid_value_info(self, *_):
        description = "Параметр должен быть целым числом."
        if not self.only_decimal:
            description += (
                " Есть поддержка чисел в бинарном, восьмеричном, шестнадцатиричном "
                "и десятиричном представлении."
            )
        if self.range_ is not None:
            range_info = f" Число должно быть >= {self.range_.start}, <= {self.range_.stop - 1}"
            if self.range_.step == 1:
                range_info += "."
            else:
                range_info += f" с шагом {self.range_.step}."
            description += range_info
        return description
