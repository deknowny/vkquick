"""
List аргумент
"""
import dataclasses
import typing as ty

from vkquick.base.text_cutter import UnmatchedArgument, TextCutter
import vkquick.utils


@dataclasses.dataclass
class List(TextCutter):
    """
    Список из типов
    """

    element: TextCutter
    """
    Тип, из которого должен строиться список
    """
    min_length: int = 1  # >=
    """
    Минимальная длина списка
    """
    max_length: ty.Optional[int] = ...  # <=
    """
    Максимальная длина списка
    """

    async def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        values = []
        remaining_string = arguments_string

        while self.max_length is Ellipsis or len(values) < self.max_length:
            remaining_string = remaining_string.lstrip()
            if remaining_string.startswith(","):
                remaining_string = remaining_string[1:]
            remaining_string = remaining_string.lstrip()
            chunk, remaining_string = await vkquick.utils.sync_async_run(
                self.element.cut_part(remaining_string)
            )

            if chunk is UnmatchedArgument:
                if len(values) > self.min_length:
                    break
                else:
                    return chunk, remaining_string

            values.append(chunk)

        return values, remaining_string

    def usage_description(self):
        part_desc = self.element.usage_description().rstrip()
        length_rule = (
            part_desc
            + f" Минимальное количество подобных аргументов больше или равно {self.min_length}, а максимальное "
        )
        if self.max_length is Ellipsis:
            max_length_desc = "не ограничено."
        else:
            max_length_desc = f"меньше или равно {self.max_length}."
        length_rule += max_length_desc
        return length_rule
