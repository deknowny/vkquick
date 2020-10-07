import re
import typing as ty

from vkquick.event_handling.reaction_argument.text_arguments import base


class SimplifiedTextArgument(base.TextArgument):
    """
    Быстрое создание своего `TextArgument`
    """

    def __init__(
        self, re_pattern: re.Pattern,
    ):
        ...
        # TODO

    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        return self.cut_part_lite(
            re.compile(r".+", flags=re.DOTALL),
            arguments_string,
            lambda x: x.group(0),
        )

    def usage_description(self, *_):
        return "Строка, содержащая любые символы"
