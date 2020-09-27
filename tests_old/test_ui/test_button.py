import vkquick as vq
import pytest


def test_line():
    """
    A Buttons line in Keyboard. Should be None
    """
    vq_button = vq.Button.line()
    assert vq_button.info is None


def test_button():
    """
    Text-buttons colors
    """
    text_button = vq.Button.text("foo")
    assert text_button.info == {"action": {"label": "foo", "type": "text"}}
    callback_button = vq.Button.callback("lol")
    assert callback_button.info == {"action": {"label": "lol", "type": "callback"}}


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


def test_color():
    """
    Test color changing
    """
    primary = vq.Button.text("foo").primary()
    secondary = vq.Button.text("foo").secondary()
    negative = vq.Button.text("foo").negative()
    positive = vq.Button.text("foo").positive()

    assert primary._info["color"] == "primary"
    assert secondary._info["color"] == "secondary"
    assert negative._info["color"] == "negative"
    assert positive._info["color"] == "positive"

    with pytest.raises(TypeError):
        vq.Button.line().negative()

    with pytest.raises(TypeError):
        vq.Button.open_link("some", link="https://www.youtube.com/watch?v=dQw4w9WgXcQ").primary()


@pytest.mark.parametrize(
    "button,info",
    [
        (
                vq.Button.text("foo", payload={"foo": "bar"}),
                {"action": {"label": "foo", "payload": '{"foo": "bar"}', "type": "text"}}
        ),
        (
                vq.Button.open_link("foo", link="https://google.com"),
                {"action": {"label": "foo", "link": "https://google.com", "type": "open_link"}}
        ),
        (
                vq.Button.location(),
                {"action": {"type": "location"}}
        ),
        (
                vq.Button.vkpay(hash_="abc"),
                {"action": {"hash": "abc", "type": "vkpay"}}
        ),
        (
                vq.Button.open_app("myapp", app_id=123, owner_id=456, hash_="abc"),
                {"action": {"label": "myapp", "app_id": 123, "owner_id": 456, "hash": "abc", "type": "open_app"}}
        ),
    ]
)
def test_button_types(button, info):
    structed_button = vq.Button.by(info)
    assert button.info == structed_button._info
