import vkquick as vq

from . import config


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
def foo(sender: vq.Sender()):
    """
    Handler to command `foo`
    """
    keyboard = vq.Keyboard(inline=True).generate(
        vq.Button.by(
            {
                "action": {
                    "type": "text",
                    "label": "foo",
                },
                "color": "primary"
            }
        )
    )
    return vq.Message("foo", keyboard=keyboard)
