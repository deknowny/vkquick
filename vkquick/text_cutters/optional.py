"""
Optional аргумент
"""
import typing as ty

from vkquick.base.text_cutter import TextCutter, UnmatchedArgument
import vkquick.utils


class Optional(TextCutter):
    """
    Опциональный тип. Если тип подходит, значит
    вернется он. Если нет -- значение по умолчанию
    """

    def __init__(
        self,
        element: TextCutter,
        /,
        *,
        default: ty.Any = None,
        default_factory: ty.Optional[ty.Callable] = None,
    ):
        """
        * `element`: Тип, который должен быть опциональным
        * `default`: Значение пол умолчанию
        Либо
        * `default_factory`: Фабрика значений по умолчанию (для мутабельных типов)
        """
        self.element = element
        self.default = default
        self.default_factory = default_factory

    async def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        chunk, remaining_string = await vkquick.utils.sync_async_run(
            self.element.cut_part(arguments_string)
        )
        if chunk is UnmatchedArgument:
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
