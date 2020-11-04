from __future__ import annotations
import inspect
import typing as ty

from vkquick.base.text_cutter import TextCutter
from vkquick.text_cutters.integer import Integer
from vkquick.text_cutters.bool_ import Bool
from vkquick.text_cutters.word import Word
from vkquick.text_cutters.list_ import Bool
from vkquick.text_cutters.bool_ import Bool


class Argument:

    def __init__(
        self,
        cutter: ty.Optional[TextCutter] = None, /,
        *,
        title: ty.Optional[str] = None,
        description: ty.Optional[str] = None,
        default
    ):
        self.cutter = cutter
        self.title = title
        self.description = description

    def __call__(self):
        return self.item



def resolve_alias(alias: ty.Any) -> TextCutter:
    if isinstance(alias, TextCutter):
        return alias
    elif inspect.isclass(alias) and issubclass(alias, TextCutter):
        return alias()
    elif alias is int:
        return Integer()
    elif alias is str:
        return Word()
    elif alias is bool:
        return Bool()
    elif isinstance(alias, ty._GenericAlias):


        # try:
        #     real_type = cutters_aliases[alias]
        # except KeyError:
        #     raise TypeError(f"Unsupported type alias `{alias}` for argument")
        # else:
        #     return real_type()
