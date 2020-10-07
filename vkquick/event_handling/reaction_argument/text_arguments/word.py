import re
import typing as ty

from vkquick.event_handling.reaction_argument.text_arguments import base


class Word(base.TextArgument):
    """
    Слово, содержащее буквы, цифры и _
    """
    def __init__(self):
        self.pattern = re.compile(r"(\w+)(?:\s+|^[,]|$)")

    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        return self.cut_part_lite(
            self.pattern, arguments_string, lambda x: x.group(1),
        )

    def usage_description(self, *_):
        return "Параметр может состоять из букв, чисел или знака нижнего подчеркивания"
