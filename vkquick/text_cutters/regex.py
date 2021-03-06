"""
Regex аргумент
"""
import re
import typing as ty

from vkquick.base.text_cutter import TextCutter


class Regex(TextCutter):
    """
    Тип через регексы. Возвращает match-группу
    """

    def __init__(
        self,
        regex: ty.Union[str, ty.Pattern],
        *,
        factory: ty.Callable[[ty.Match], ty.Any] = lambda match: match,
    ):
        """
        * `regex`: Регекс строкой либо через `re.compile`
        * `factory`: Фабрика для матч группы
        """
        self.pattern = re.compile(regex) if isinstance(regex, str) else regex
        self.factory = factory

    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        return self.cut_part_lite(
            self.pattern, arguments_string, self.factory
        )

    def usage_description(self) -> str:
        return f"Аргумент должен подходить под шаблон {self.pattern.pattern}."