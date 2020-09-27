import typing as ty

from . import base


class Integer(base.TextArgument):
    """
    Целое знаковое число

    # TODO
    """

    description = "Целое знаковое число"

    def cut_part(
        self, string: str
    ) -> ty.Tuple[ty.Union[ty.Any, base.PacifierArgument], str]:
        return self.quick_cutting(r"\d+", string)
