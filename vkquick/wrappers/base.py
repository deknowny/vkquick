import dataclasses
import typing as ty

import attrdict

import vkquick.utils


@dataclasses.dataclass
class Wrapper:
    """
    Wrapper -- специальная обертка на объекты ВК
    """
    scheme: attrdict.AttrMap

    def __post_init__(self):
        self._shortcuts: ty.Dict[str, ty.Any] = {}

    def add_field_shortcut(self, alias: str, value: ty.Any) -> None:
        """
        Добавляет шорткаты на некоторые поля из `scheme`
        """
        setattr(self, alias, value)
        self._shortcuts[alias] = value

    def __format__(self, format_spec: str) -> str:
        inserted_values = vkquick.utils.SafeDict(
            scheme=self.scheme,
            **self._shortcuts
        )
        return format_spec.format_map(inserted_values)