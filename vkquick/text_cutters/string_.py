"""
String аргумент
"""
import re
import typing as ty

import vkquick.base.text_cutter
import vkquick.base.text_values


class String(
    vkquick.base.text_cutter.TextCutter,
    vkquick.base.text_values.TextBase,
):
    """
    Любая последовательность символов
    """

    def __init__(
        self, *, max_length: ty.Optional[int] = None, min_length: int = 1
    ):
        """
        * `max_length`: Максимальная длина строки
        * `min_length`: Минимальная длина строки
        """
        self.pattern = re.compile(r".+", flags=re.DOTALL)
        super().__init__(max_length, min_length)

    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        parsed_result = self.cut_part_lite(
            self.pattern, arguments_string, lambda x: x.group(0),
        )
        return self.check_range(*parsed_result)

    def usage_description(self):
        desc = "Аргумент является строкой, содержащей любые символы. "  # Пробел стоит специально
        return self.create_length_rule(desc)
