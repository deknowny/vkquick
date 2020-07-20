from __future__ import annotations

from .button import Button
from .ui import UI


class Keyboard(UI):
    """
    Клавиатура для messages.send.

    Вы можете создать клаивиатуру вручную
    через JSON по унаследованному `vkquick.tools.ui.UI.by`
    либо воспользоваться конструктором `Keyboard.generate`

    ## Пример
    Инлайн клавиатура из 4 кнопок в два ряда,
    присылаемая по команде ```/keyboard```

        import vkquick as vq


        @vq.Cmd(names=["keyboard"], prefs=["/"])
        @vq.Reaction("message_new")
        def keyboard():
            kb = vq.Keyboard(inline=True).generate(
                vq.Button.text("foo").positive(),
                vq.Button.text("bar").negative(),
                vq.Button.line(),
                vq.Button.text("fizz").secondary(),
                vq.Button.text("bazz").primary(),
            )

            return vq.Message("Your Keyboard:", keyboard=kb)

    Аналогичная клавиатуры через метод `Keyboard.add`:

        import vkquick as vq


        @vq.Cmd(names=["keyboard"], prefs=["/"])
        @vq.Reaction("message_new")
        def keyboard():
            kb = vq.Keyboard(inline=True)
            kb.add(vq.Button.text("foo").positive())
            kb.add(vq.Button.text("bar").negative())
            kb.add(vq.Button.line())
            kb.add(vq.Button.text("fizz").secondary())
            kb.add(vq.Button.text("bazz").primary())

            return vq.Message("Your Keyboard:", keyboard=kb)
    """

    def __init__(self, *, one_time: bool = True, inline: bool = False):
        self.info = dict(inline=inline, buttons=[[]])
        if not inline:
            self.info.update(one_time=one_time)

    @classmethod
    def empty(cls):
        """
        Возвращает пустую клавиатуру
        (используется, чтобы убрать one_time=False кливиатуру)
        """
        return '{"buttons":[],"one_time":true}'

    def add(self, button: Button = Button.line()) -> Keyboard:
        """
        Добавляет в клавиатуру кнопку или пустую строку
        """
        if button.info is None:
            if self.info["buttons"][-1]:
                self.info["buttons"].append([])
            else:
                raise ValueError(
                    "Can't add Button.line() after Button.line()"
                )
        else:
            self.info["buttons"][-1].append(button.info)

        return self

    def generate(self, *buttons: Button) -> Keyboard:
        """
        Создает клавиатуру по списку кнопок и `vkquick.tools.button.Button.line`'ов
        """
        for button in buttons:
            self.add(button)

        return self
