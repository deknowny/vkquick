import dataclasses
import typing as ty

import attrdict


@dataclasses.dataclass
class Wrapper:
    """
    Wrapper -- специальная обертка на объекты ВК
    """
    scheme: attrdict.AttrMap

    def __post_init__(self):
        self.shortcuts: ty.Dict[str, ty.Any] = {}

    def add_field_shortcut(self, alias: str, value: ty.Any) -> None:
        """
        Добавляет шорткаты на некоторые поля из `scheme`
        """
        setattr(self, alias, value)
        self.shortcuts[alias] = value
