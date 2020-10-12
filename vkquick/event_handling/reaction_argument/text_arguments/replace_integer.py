import re
import typing as ty

import vkquick.event_handling.reaction_argument.text_arguments.base


class ReplaceInteger(
    vkquick.event_handling.reaction_argument.text_arguments.base.TextArgument
):
    """
    Целое число.
    """

    def __init__(
        self, *, old_value: str, new_value: str
    ):
        self.old_value = old_value
        self.new_value = new_value
        self.pattern = re.compile(r"\w+")

    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        value, parsed_string = self.cut_part_lite(
            self.pattern, arguments_string, lambda x: x.group(0),
        )
        if (
            value
            is not vkquick.event_handling.reaction_argument.text_arguments.base.UnmatchedArgument
            and value.replace(self.old_value, self.new_value).isdigit()
        ):
            return int(value.replace(self.old_value, self.new_value)), parsed_string

        return (
            vkquick.event_handling.reaction_argument.text_arguments.base.UnmatchedArgument,
            parsed_string
        )

    def usage_description(self):
        description = f"Аргумент должен быть числом. Так же, можно сократить написав в любом месте в числе {repr(self.old_value)} оно автоматически замениться на {repr(self.new_value)}"
        return description
