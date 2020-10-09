import re
import typing as ty

import vkquick.event_handling.reaction_argument.text_arguments.base
import vkquick.event_handling.reaction_argument.text_arguments._text_base


class Word(
    vkquick.event_handling.reaction_argument.text_arguments.base.TextArgument,
    vkquick.event_handling.reaction_argument.text_arguments._text_base.TextBase,
):
    """
    Слово, содержащее буквы, цифры и _
    """

    def __init__(
        self, max_length: ty.Optional[int] = None, min_length: int = 1
    ):
        self.pattern = re.compile(r"\w+")
        super().__init__(max_length, min_length)

    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        parsed_result = self.cut_part_lite(
            self.pattern, arguments_string, lambda x: x.group(0),
        )
        return self.check_range(*parsed_result)

    def usage_description(self, *_):
        desc = "Параметр может состоять из букв, чисел или знака нижнего подчеркивания. "
        return self.usage_description(desc)
