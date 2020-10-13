import dataclasses
import typing as ty

import vkquick.utils


@dataclasses.dataclass
class Wrapper:
    """
    Wrapper -- специальная обертка на объекты ВК
    """

    scheme: vkquick.utils.AttrDict

    def __post_init__(self):
        self._shortcuts: ty.Dict[str, ty.Any] = {}

    def add_scheme_shortcut(self, alias: str, value: ty.Any) -> None:
        """
        Добавляет шорткаты на некоторые поля из `scheme`
        """
        setattr(self, alias, value)
        self._shortcuts[alias] = value

    def __format__(self, format_spec: str) -> str:
        inserted_values = vkquick.utils.SafeDict(
            scheme=self.scheme, **self._shortcuts
        )
        return format_spec.format_map(inserted_values)

    def __str__(self):
        shortcuts = [
            f"{name}={value!r}"
            for name, value in self._shortcuts.items()
        ]
        shortcuts = ", ".join(shortcuts)

        return f"{self.__class__.__name__}({shortcuts})"


