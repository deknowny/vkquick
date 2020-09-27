import abc
import re
import typing as ty


PacifierArgument = ty.TypeVar("PacifierArgument")


class TextArgument(abc.ABC):
    """
    Текстовый аргумент для обработчика события.
    Указывается в аннотациях. Может быть указан не объектом
    текущего класса, а самим классом, тогда инициализация объекта
    должна быть возможна без аргументов, т.е.

        foo: MyType

    Эквивалентно

        foo: MyType()
    """

    description = "Отсуствует"

    @abc.abstractmethod
    def cut_part(
        self, string: str
    ) -> ty.Tuple[ty.Union[ty.Any, PacifierArgument], str]:
        """
        На вход принимает строку и проверяет, явлется ли объект ее началом.
        В случае провала, возвращается `PacifierArgument`
        """

    @staticmethod
    def quick_cutting(
        pattern: str, string: str
    ) -> ty.Tuple[ty.Union[ty.Match, PacifierArgument], str]:
        """
        Быстрый "вырез" нужного значения из строки
        по шаблону `pattern` из строки `string`
        """
        cut_value = re.match(rf"\s+({pattern})", string)
        if cut_value is None:
            return PacifierArgument, string
        return cut_value.group(0), string[cut_value.end():]
