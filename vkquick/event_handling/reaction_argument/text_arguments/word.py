import re
import typing as ty

from . import base


class Word(base.TextArgument):
    """
    Слово, содержащее буквы, цифры и _
    """

    always_be_instance = True

    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        return self.cut_part_lite(re.compile(r"\w+"), arguments_string, lambda x: x.group(0))
