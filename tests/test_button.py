import pytest

import vkquick as vq


class TestButton:
    def test_colors(self):
        assert vq.Button.text("a").primary().scheme["color"] == "primary"
        assert vq.Button.text("a").negative().scheme["color"] == "negative"
        assert vq.Button.text("a").positive().scheme["color"] == "positive"
        assert vq.Button.text("a").negative().scheme["color"] == "negative"

    def test_payload_convert(self):
        button = vq.Button.text("a")
        assert "payload" not in button.scheme

        button = vq.Button.text("a", payload={"foo": 123})
        assert button.scheme["action"]["payload"] == '{"foo":123}'

        button = vq.Button.text("a", payload='{"foo":123}')
        assert button.scheme["action"]["payload"] == '{"foo":123}'

        with pytest.raises(TypeError):
            vq.Button.text("a", payload=1)

    def test_every_type(self):
        assert vq.Button.text("a").scheme["action"]["type"] == "text"
        assert (
            vq.Button.open_link("a", link="b").scheme["action"]["type"]
            == "open_link"
        )
        assert vq.Button.location().scheme["action"]["type"] == "location"
        assert vq.Button.vkpay(hash_="a").scheme["action"]["type"] == "vkpay"
        assert (
            vq.Button.open_app("a", app_id=1, owner_id=1, hash_="a").scheme[
                "action"
            ]["type"]
            == "open_app"
        )
        assert vq.Button.callback("a").scheme["action"]["type"] == "callback"
