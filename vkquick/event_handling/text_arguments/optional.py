import typing as ty

import vkquick.base.text_argument
import vkquick.utils


class Optional(vkquick.base.text_argument.TextArgument):
    """
    Любая последовательность символов
    """

    def __init__(
        self,
        element: vkquick.base.text_argument.TextArgument,
        /,
        *,
        default: ty.Any = None,
        default_factory: ty.Optional[ty.Callable] = None,
    ):
        self.element = element
        self.default = default
        self.default_factory = default_factory

    async def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        chunk, remaining_string = await vkquick.utils.sync_async_run(
            self.element.cut_part(arguments_string)
        )
        if chunk is vkquick.base.text_argument.UnmatchedArgument:
            if self.default_factory is None:
                placeholder = self.default
            else:
                placeholder = self.default_factory()

            return placeholder, remaining_string

        return chunk, remaining_string

    def usage_description(self):
        element_desc = self.element.usage_description().rstrip()
        addiction = "Может быть пропущен."
        desc = element_desc + addiction
        return desc
