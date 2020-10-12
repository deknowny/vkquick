import re
import typing as ty

import vkquick.event_handling.reaction_argument.text_arguments.base
import vkquick.event_handling.reaction_argument.text_arguments.text_values_base


class String(
    vkquick.event_handling.reaction_argument.text_arguments.base.TextArgument,
    vkquick.event_handling.reaction_argument.text_arguments.text_values_base.TextBase,
):
    """
    Любая последовательность символов
    """

    def __init__(
        self, *, max_length: ty.Optional[int] = None, min_length: int = 1
    ):
        self.pattern = re.compile(r".+", flags=re.DOTALL)
        super().__init__(max_length, min_length)

    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        parsed_result = self.cut_part_lite(
            self.pattern, arguments_string, lambda x: x.group(0),
        )
        return self.check_range(*parsed_result)

    def usage_description(self):
        desc = "Строка, содержащая любые символы. "  # Пробел стоит специально
        return self.create_length_rule(desc)
