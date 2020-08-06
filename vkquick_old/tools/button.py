from __future__ import annotations
from typing import Union, Optional
import json
from json.decoder import JSONDecodeError


from .ui import UI


def color(color_name: str, doc: str):
    def colorized(self: Button):
        error_text = "Colors unsupported for button type {}"
        if self.info is None:
            raise TypeError(error_text.format("Button.line()"))
        elif action_type := self.info["action"]["type"] not in (
            "text",
            "callback",
        ):
            raise TypeError(error_text.format(action_type))

        self.info["color"] = color_name
        return self

    colorized.__doc__ = doc
    return colorized


def validate_payload(payload: Optional[Union[str, dict]]) -> None:
    if isinstance(payload, str):
        try:
            json.loads(payload)
        except JSONDecodeError as err:
            raise ValueError(
                "Invalid payload struct, "
                "should be JSON format, "
                "but get JSONDecodeError: "
                f"{err}"
            )


class Button(UI):
    """
    Клавиатурная кнопка.
    Работает в `vkquick.tools.keyboard.Keyboard`
    и `vkquick.tools.element.Element`

    Пример текстовой кнопки цвета `primary`
    ```python
    Button.text("Текст кнопки").primary()
    ```

    Пример кнопки, открывающей страницу google
    ```python
    Button.open_link("google", link="https://google.com")
    ```
    """

    positive = color("positive", doc="Зеленая кнопка (для обеих тем)")
    negative = color("negative", doc="красная кнопка (для обеих тем)")
    primary = color("primary", doc="Синяя кнопка для белой, белая для темной")
    secondary = color(
        "secondary", doc="Белая кнопка для светлой темы, серая для темной"
    )

    @staticmethod
    def _validate_payload(payload):
        """
        Вызывает исключение в случае ошибки валидации, иначе возвращает None.
        """
        if not isinstance(payload, (str, dict)):
            raise TypeError(
                "Payload should be "
                "dumped dict to string "
                "or dict, not "
                f"{type(payload)}"
            )

    @staticmethod
    def _to_raw_payload(payload) -> str:
        if isinstance(payload, dict):
            return json.dumps(payload)
        return payload

    def __init__(
        self, info: dict, payload: Optional[Union[str, dict]] = None
    ):
        if payload is not None:
            self._validate_payload(payload)
            payload = self._to_raw_payload(payload)
            info.update(payload=payload)
        self.info: Optional[dict] = dict(action=info)

    @classmethod
    def text(
        cls, label: str, *, payload: Optional[Union[str, dict]] = None
    ) -> Button:
        """
        Кнопка типа text
        """
        return cls(info={"label": label, "type": "text"}, payload=payload)

    @classmethod
    def open_link(
        cls,
        label: str,
        *,
        link: str,
        payload: Optional[Union[str, dict]] = None,
    ) -> Button:
        """
        Кнопка типа open_link
        """
        return cls(
            info={"label": label, "link": link, "type": "open_link"},
            payload=payload,
        )

    @classmethod
    def location(
        cls, *, payload: Optional[Union[str, dict]] = None
    ) -> Button:
        """
        Кнопка типа location
        """
        return cls(info={"type": "location"}, payload=payload)

    @classmethod
    def vkpay(
        cls, *, hash_: str, payload: Optional[Union[str, dict]] = None
    ) -> Button:
        """
        Кнопка типа vkpay
        """
        return cls(info={"hash": hash_, "type": "vkpay"}, payload=payload)

    @classmethod
    def open_app(
        cls,
        label: str,
        *,
        app_id: int,
        owner_id: int,
        hash_: str,
        payload: Optional[Union[str, dict]] = None,
    ) -> Button:
        """
        Кнопка типа open_app
        """
        return cls(
            info={
                "label": label,
                "app_id": app_id,
                "owner_id": owner_id,
                "hash": hash_,
                "type": "open_app",
            },
            payload=payload,
        )

    @classmethod
    def callback(
        cls, label: str, *, payload: Optional[Union[str, dict]] = None
    ) -> Button:
        """
        Кнопка типа callback
        """
        return cls(info={"label": label, "type": "callback"}, payload=payload)

    @classmethod
    def line(cls) -> Button:
        instance = cls(info={})
        instance.info = None
        return instance
