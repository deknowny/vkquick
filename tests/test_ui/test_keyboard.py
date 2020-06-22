import vkquick as vq
import pytest


def test_all_inits():
    kb_dict = {
        "one_time": True,
        "inline": False,
        "buttons": [
            [
                {
                    "action": {
                        "type": "text",
                        "label": "foo",
                    },
                    "color": "primary"
                },
                {
                    "action": {
                        "type": "text",
                        "label": "bar",
                    },
                    "color": "secondary"
                }
            ],
            [
                {
                    "action": {
                        "type": "open_link",
                        "label": "google",
                        "link": "https://google.com"
                    }
                }
            ]
        ]
    }
    kb_vq1 = vq.Keyboard().generate(
        vq.Button.text("foo").primary(),
        vq.Button.text("bar").secondary(),
        vq.Button.line(),
        vq.Button.open_link("google", link="https://google.com")
    )
    kb_vq2 = vq.Keyboard()
    kb_vq2.add(vq.Button.text("foo").primary())
    kb_vq2.add(vq.Button.text("bar").secondary())
    kb_vq2.add(vq.Button.line())
    kb_vq2.add(vq.Button.open_link("google", link="https://google.com"))

    kb_vq3 = vq.Keyboard.by(kb_dict)

    assert kb_dict == kb_vq1.info == kb_vq2.info == kb_vq3.info
    assert repr(kb_vq1) == repr(kb_vq2)


def test_two_lines():
    with pytest.raises(ValueError):
        kb = vq.Keyboard().generate(
            vq.Button.text("foo"),
            vq.Button.line(),
            vq.Button.line(),
            vq.Button.text("bar")
        )
    with pytest.raises(ValueError):
        kb = vq.Keyboard().generate(
            vq.Button.line()
        )

def test_info():
    kb1 = vq.Keyboard() # one_time=True
    kb2 = vq.Keyboard(one_time=False)
    kb3 = vq.Keyboard(inline=True)

    kb1_dict = {
        "one_time": True,
        "inline": False,
        "buttons": [[]]
    }
    kb2_dict = {
        "one_time": False,
        "inline": False,
        "buttons": [[]]
    }
    kb3_dict = {
        "inline": True,
        "buttons": [[]]
    }

    assert kb1.info == kb1_dict
    assert kb2.info == kb2_dict
    assert kb3.info == kb3_dict
