from __future__ import annotations

import dataclasses
import functools
import typing

from vkquick.json_parsers import json_parser_policy
from vkquick.types import DecoratorFunction

if typing.TYPE_CHECKING:  # pragma: no cover
    from vkquick.chatbot.storages import CallbackButtonPressed, NewMessage


@dataclasses.dataclass
class _ButtonHandler:
    handler: typing.Callable


@dataclasses.dataclass
class ButtonOnclickHandler(_ButtonHandler):
    handler: typing.Callable[[NewMessage, ...], typing.Awaitable]


@dataclasses.dataclass
class ButtonCallbackHandler(_ButtonHandler):
    handler: typing.Callable[[CallbackButtonPressed, ...], typing.Awaitable]


class InitializedButton:
    def __init__(self, **scheme) -> None:
        self.scheme = {"action": scheme}

    def _on_action(
        self, handler: _ButtonHandler, **kwargs
    ) -> InitializedButton:
        if self.scheme["action"].get("payload"):
            raise ValueError(
                "Payload has been already set. "
                "You can set only or onclick handler or "
                "custom payload, not bath at hte same time"
            )
        schema = dict(command=handler.handler.__name__, args=kwargs)
        self.scheme["action"]["payload"] = json_parser_policy.dumps(schema)
        return self


ClickableOrCallable = typing.TypeVar("ClickableOrCallable")


class _ColoredButton(InitializedButton):
    def positive(self: ClickableOrCallable) -> ClickableOrCallable:
        """
        Зеленая кнопка (для обеих тем)
        """
        self.scheme["color"] = "positive"
        return self

    def negative(self: ClickableOrCallable) -> ClickableOrCallable:
        """
        Розовая (красная) кнопка (для обеих тем)
        """
        self.scheme["color"] = "negative"
        return self

    def primary(self: ClickableOrCallable) -> ClickableOrCallable:
        """
        Синяя кнопка для белой, белая для темной
        """
        self.scheme["color"] = "primary"
        return self

    def secondary(self: ClickableOrCallable) -> ClickableOrCallable:
        """
        Белая кнопка для светлой темы, серая для темной
        """
        self.scheme["color"] = "secondary"
        return self


class _ClickableColoredButton(_ColoredButton):
    def on_click(
        self, handler: ButtonOnclickHandler, **kwargs
    ) -> InitializedButton:
        return self._on_action(handler, **kwargs)


class _CallableColoredButton(_ColoredButton):
    def on_called(self, handler: ButtonCallbackHandler, **kwargs):
        return self._on_action(handler, **kwargs)


class _UncoloredButton(InitializedButton):
    ...


def _convert_payload(func: DecoratorFunction) -> DecoratorFunction:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "payload" in kwargs:
            if isinstance(kwargs["payload"], dict):
                kwargs["payload"] = json_parser_policy.dumps(
                    kwargs["payload"]
                )
            elif not isinstance(kwargs["payload"], str):
                raise TypeError(
                    "Invalid type for payload. "
                    "Payload can be only str, "
                    "dict or not passed"
                )
        return func(*args, **kwargs)

    return wrapper


class Button:
    @classmethod
    @_convert_payload
    def text(
        cls,
        label: str,
        *,
        payload: typing.Optional[typing.Union[str, dict]] = None,
    ) -> _ClickableColoredButton:
        """
        Кнопка типа `text`
        """
        return _ClickableColoredButton(
            label=label, type="text", payload=payload
        )

    @classmethod
    @_convert_payload
    def open_link(
        cls,
        label: str,
        *,
        link: str,
        payload: typing.Optional[typing.Union[str, dict]] = None,
    ) -> _UncoloredButton:
        """
        Кнопка типа `open_link`
        """
        return _UncoloredButton(
            label=label,
            link=link,
            type="open_link",
            payload=payload,
        )

    @classmethod
    @_convert_payload
    def location(
        cls, *, payload: typing.Optional[typing.Union[str, dict]] = None
    ) -> _UncoloredButton:
        """
        Кнопка типа `location`
        """
        return _UncoloredButton(type="location", payload=payload)

    @classmethod
    @_convert_payload
    def vkpay(
        cls,
        *,
        hash_: str,
        payload: typing.Optional[typing.Union[str, dict]] = None,
    ) -> _UncoloredButton:
        """
        Кнопка типа `vkpay`
        """
        return _UncoloredButton(hash=hash_, type="vkpay", payload=payload)

    @classmethod
    @_convert_payload
    def open_app(
        cls,
        label: str,
        *,
        app_id: int,
        owner_id: int,
        hash_: str,
        payload: typing.Optional[typing.Union[str, dict]] = None,
    ) -> _UncoloredButton:
        """
        Кнопка типа `open_app`
        """
        return _UncoloredButton(
            label=label,
            app_id=app_id,
            owner_id=owner_id,
            hash=hash_,
            type="open_app",
            payload=payload,
        )

    @classmethod
    @_convert_payload
    def callback(
        cls,
        label: str,
        *,
        payload: typing.Optional[typing.Union[str, dict]] = None,
    ) -> _CallableColoredButton:
        """
        Кнопка типа `callback`
        """
        return _CallableColoredButton(
            label=label, type="callback", payload=payload
        )
