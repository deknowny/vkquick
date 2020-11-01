import dataclasses
import typing as ty

import vkquick.utils


@dataclasses.dataclass
class Wrapper:
    """
    Wrapper -- специальная обертка на объекты ВК для более удобного
    взаимодействия. Например, можно собрать объект фотографии
    через файл фотографии (т.е. загрузить) или же комфортно
    взаимодействовать с полями пользователя (сделать упоминание пользователя,
    зная лишь его ID)
    """

    scheme: vkquick.utils.AttrDict
    """
    Словарь объекта, с которым можно взаимодействовать
    """

    def __post_init__(self):
        self._shortcuts: ty.Dict[str, ty.Any] = {}

    def add_scheme_shortcut(self, alias: str, value: ty.Any) -> None:
        """
        Добавляет шорткаты на некоторые поля из `scheme`
        """
        setattr(self, alias, value)
        self._shortcuts[alias] = value

    def __format__(self, format_spec: str) -> str:
        format_spec = format_spec.replace(">", "}")
        format_spec = format_spec.replace("<", "{")
        inserted_values = vkquick.utils.SafeDict(
            scheme=self.scheme, **self._shortcuts
        )
        return format_spec.format_map(inserted_values)

    def format(self, format_spec: str) -> str:
        """
        Вызывает формат объекта
        """
        return self.__format__(format_spec)

    def __str__(self):
        shortcuts = [
            f"{name}={value!r}" for name, value in self._shortcuts.items()
        ]
        shortcuts = ", ".join(shortcuts)

        return f"{self.__class__.__name__}({shortcuts})"
