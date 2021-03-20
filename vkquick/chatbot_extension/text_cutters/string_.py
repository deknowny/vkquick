"""
String аргумент
"""
import re
import typing as ty

from vkquick.base.text_cutter import TextCutter
from vkquick.base.text_values import TextBase


class String(
    TextCutter,
    TextBase,
):
    """
    Любая последовательность символов
    """

    def __init__(
        self,
        *,
        max_length: ty.Optional[int] = None,
        min_length: int = 1,
        dotall: bool = True
    ):
        """
        * `max_length`: Максимальная длина строки
        * `min_length`: Минимальная длина строки
        * `dotall`: Использовать ли `re.DOTALL` флаг длс регулярки
        """
        flags = re.DOTALL if dotall else 0
        self.pattern = re.compile(r".+", flags=flags)
        super().__init__(max_length, min_length)

    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        parsed_result = self.cut_part_lite(
            self.pattern,
            arguments_string,
            lambda x: x.group(0),
        )
        return self.check_range(*parsed_result)

    def usage_description(self):
        desc = "Аргумент является строкой, содержащей любые символы"
        if self.pattern.flags & re.DOTALL:
            desc += ". "  # Пробел стоит специально
        else:
            desc += ", кроме новой строки. "
        return self.create_length_rule(desc)
