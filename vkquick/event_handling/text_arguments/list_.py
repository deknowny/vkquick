import dataclasses
import typing as ty

import vkquick.event_handling.text_arguments.base


@dataclasses.dataclass
class List(vkquick.event_handling.text_arguments.base.TextArgument):
    """
    Список
    """

    element: vkquick.event_handling.text_arguments.base.TextArgument
    min_length: int = 1
    max_length: ty.Optional[int] = None

    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        values = []
        while True:

            value, parsed_string = self.cut_part_lite(
                self.pattern, arguments_string, lambda x: x.group(0),
            )

    def usage_description(self):
        desc = "Параметр может состоять из букв, чисел или знака нижнего подчеркивания. "  # Пробел стоит специально
        return self.create_length_rule(desc)
