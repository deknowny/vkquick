from __future__ import annotations

import typing

from vkquick.chatbot.base.ui_builder import UIBuilder
from vkquick.chatbot.ui_builders.button import InitializedButton


class Keyboard(UIBuilder):
    """
    Генерирует клавиатуру на основе переданных кнопок.
    Чтобы добавить новый ряд, передайте Ellipsis (три точки)
    вместо кнопки. Клавиатуру можно создать и в другом стиле:
    вызывая `.add()` для каждой новой кнопки и `.new_line()`
    для перехода на следующий ряд

    Настройки `one_time` и `inline` передаются при самой инициализации

    Объект можно напрямую передать в поле `keyboard`
    при отправке сообщения
    """

    def __init__(
        self,
        *buttons: typing.Union[InitializedButton, type(Ellipsis)],
        one_time: bool = True,
        inline: bool = False
    ) -> None:
        self.scheme = {"inline": inline, "buttons": [[]]}
        if not inline:
            self.scheme.update(one_time=one_time)

        self._build(*buttons)

    @staticmethod
    def empty() -> str:
        """
        Returns:
            Пустую клавиатуру. Используйте, чтобы удалить текущую
        """
        return '{"buttons":[],"one_time":true}'

    def add(self, button: InitializedButton) -> Keyboard:
        """
        Добавляет в клавиатуру кнопку

        Arguments:
            button: Кнопка, которую надо добавить

        Returns:
            Текущая клавиатура
        """
        self.scheme["buttons"][-1].append(button.scheme)
        return self

    def new_line(self) -> Keyboard:
        """
        Добавляет новый ряд клавиатуре
        """
        if not self.scheme["buttons"][-1]:
            raise ValueError("Can't add a new line if the last line is empty")
        self.scheme["buttons"].append([])
        return self

    def _build(
        self, *buttons: typing.Union[InitializedButton, type(Ellipsis)]
    ) -> None:
        """
        Вспомогательный метод для построения рядов кнопок

        Arguments:
            buttons: Кнопки или Ellipsis (для новой линии)
        """
        for button in buttons:
            if button is Ellipsis:
                self.new_line()
            else:
                self.add(button)
