from functools import wraps

import vkquick as vq
import pytest


def test_line():
    """
    A Buttons line in Keyboard. Should be None
    """
    vq_button = vq.Button.line()
    assert vq_button.info is None


def test_color():
    """
    Text-buttons colors
    """
    vq_button = vq.Button.text("foo")


def test_payload():
    """
    Test payload
    """
    # No payload
    vq_button = vq.Button.text("foo")
    assert "payload" not in vq_button.info["action"]

    # Payload by dict
    vq_button = vq.Button.text(
        "foo", payload={"foo": 123}
    )
    assert (
        vq_button.info["action"]["payload"] ==
        '{"foo": 123}'
    )

    # Payload by valid string
    vq_button = vq.Button.text(
        "foo", payload='{"foo": 123}'
    )
    assert (
        vq_button.info["action"]["payload"] ==
        '{"foo": 123}'
    )

    # Payload by invalid string
    with pytest.raises(ValueError):
        vq_button = vq.Button.text(
            "foo", payload='{foo": 123}'
        )


def test_color():
    """
    Test color changing
    """
    primary = vq.Button.text("foo").primary()
    secondary = vq.Button.text("foo").secondary()
    negative = vq.Button.text("foo").negative()
    positive = vq.Button.text("foo").positive()

    assert primary.info["color"] == "primary"
    assert secondary.info["color"] == "secondary"
    assert negative.info["color"] == "negative"
    assert positive.info["color"] == "positive"


def button_type(func):
    """
    Decorator for button types testing

    """
    @wraps(func)
    def wrapper():
        vq_button, dict_button = func()
        button_by_struct = vq.Button.by(dict_button)

        assert vq_button.info == dict_button
        assert repr(button_by_struct) == repr(vq_button)

@button_type
def test_text():
    """
    A button with text
    """
    return (
        vq.Button.text("foo", payload={"foo": "bar"}),
        {
            "action": {
                "label": "foo",
                "payload": '{"foo": "bar"}',
                "type": "text"
            }
        }
    )


@button_type
def test_open_link():
    """
    An open_link-button
    """
    return (
        vq.Button.open_link("foo", link="https://google.com"),
        {
            "action": {
                "label": "foo",
                "link": "https://google.com",
                "type": "open_link"
            }
        }
    )


@button_type
def test_location():
    """
    A location-button
    """
    return (
        vq.Button.location(),
        {
            "action": {
                "label": "foo"
            }
        }
    )


def test_vkpay():
    """
    A vkpay-button
    """
    return (
        vq.Button.vkpay(hash_="abc"),
        {
            "action": {
                "hash": "abc",
                "type": "vkpay"
            }
        }
    )


def test_open_app():
    """
    An open_app-button
    """
    return (
        vq.Button.open_app(
            "myapp",
            app_id=123,
            owner_id=456,
            hash_="abc"
        ),
        {
            "action": {
                "label": "myapp",
                "app_id": 123,
                "owner_id": 456,
                "hash": "abc",
                "type": "vkpay"
            }
        }
    )
