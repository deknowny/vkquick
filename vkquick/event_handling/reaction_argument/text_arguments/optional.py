import warnings
import typing as ty

from vkquick.event_handling.reaction_argument.text_arguments import base
import vkquick.utils

class Optional(base.TextArgument):
    """
    Делает аргумент опциональным
    """

    def __init__(self, element, default=None, /):
        self.element = element
        self.default = default

    async def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        values = await vkquick.utils.sync_async_run(
            self.element.cut_part(arguments_string)
        )
        if values[0] is not base.UnmatchedArgument:
            return values
        return self.default, arguments_string

    async def usage_description(self) -> str:
        description = "Параметер является необезательным"
        return description
