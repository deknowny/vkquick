from __future__ import annotations
from typing import Union
from json import dumps

from .ui import UI


class Button(UI):
    """
    Keyboards button. Aviable for Keyboard and Templates
    """
    def __new__(cls, **info):
        self = object.__new__(cls)
        self.__init__(info)
        return self

    def __init__(self, info) -> None:
        self.info = dict(
            action=info
        )
        self.info = {"action": {**info}}

    def positive(self) -> Button:
        """
        Green button
        """
        self.info["color"] = "positive"
        return self

    def negative(self) -> Button:
        """
        Red button
        """
        self.info["color"] = "negative"
        return self

    def secondary(self) -> Button:
        """
        White button
        """
        self.info["color"] = "secondary"
        return self

    def primary(self) -> Button:
        """
        Blue button
        """
        self.info["color"] = "primary"
        return self

    @classmethod
    def line(cls) -> Button:
        """
        Add Buttons line
        """
        self = cls._button_init()
        self.info = None

        return self

    @classmethod
    def text(
        cls, label: str, *,
        payload: Union[str, dict] = "{}"
    ) -> Button:
        return cls.__new__(
            cls,
            type="text",
            label=label,
            payload=cls._payload_convert(payload)
        )

    @classmethod
    def open_link(
        cls, *,
        link: str,
        label: str,
        payload: Union[str, dict] = "{}"
    ) -> Button:
        return cls.__new__(
            cls,
            type="open_link",
            link=link,
            label=label,
            payload=cls._payload_convert(payload)
        )

    @classmethod
    def location(
        cls, *,
        payload: Union[str, dict] = "{}"
    ) -> Button:
        return cls.__new__(
            cls,
            type="location",
            payload=cls._payload_convert(payload)
        )

    @classmethod
    def vkpay(
        cls, *,
        hash_: str,
        payload: Union[str, dict] = "{}"
    ) -> Button:
        return cls.__new__(
            cls,
            type="vkpay",
            hash=hash_,
            payload=cls._payload_convert(payload)
        )

    @classmethod
    def open_app(
        cls, label: str, *,
        app_id: int,
        owner_id: int,
        hash_: str,
        payload: Union[str, dict] = "{}"
    ) -> Button:
        return cls.__new__(
            cls,
            type="open_app",
            label=label,
            app_id=app_id,
            owner_id=owner_id,
            hash=hash_,
            payload=cls._payload_convert(payload)
        )

    @staticmethod
    def _payload_convert(data: Union[dict, str]):
        if isinstance(data, dict):
            return dumps(data, ensure_ascii=False)
        else:
            return str(data)
