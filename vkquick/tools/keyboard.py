from __future__ import annotations
from typing import Optional
from json import dumps

from .button import Button
from .ui import UI


class Keyboard(UI):
    """
    messages.send keyboard.
    Create VK Keyboard by dict or buttons list
    """
    def __init__(
        self,
        one_time: bool = True,
        inline: bool = False
    ):
        if inline:
            self.info = dict(
                inline=inline,
                buttons=[[]]
            )
        else:
            self.info = dict(
                one_time=one_time,
                inline=inline,
                buttons=[[]]
            )
    def add(self, button: Button):
        """
        Add a button or a line
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
        Create keyboard by Buttons instances
        """
        for button in buttons:
            self.add(button)

        return self
