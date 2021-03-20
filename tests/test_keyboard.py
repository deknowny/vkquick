import pytest

import vkquick as vq


class TestKeyboard:
    def test_adding(self):
        button1 = vq.Button.text("a").primary()
        button2 = vq.Button.text("a").secondary()
        kb = vq.Keyboard()
        kb.add(button1)
        kb.add(button2)
        kb.add_line()
        kb.add(button1)
        kb.add(button2)
        assert kb.scheme["buttons"] == [
            [button1.scheme, button2.scheme],
            [button1.scheme, button2.scheme],
        ]

    def test_incorrect_lines(self):
        kb = vq.Keyboard()
        with pytest.raises(ValueError):
            kb.add_line()

        kb = vq.Keyboard().build(vq.Button.text("a").primary())
        with pytest.raises(ValueError):
            kb.add_line()
            kb.add_line()

    def test_building(self):
        button1 = vq.Button.text("a").primary()
        button2 = vq.Button.text("b").secondary()
        kb = vq.Keyboard().build(button1, ..., button2,)
        assert kb.scheme["buttons"] == [[button1.scheme], [button2.scheme]]
