import vkquick as vq

from . import config


@vq.Cmd(names=["my name is"])
@vq.Reaction("message_new")
def foo(name: str):
    return f"your name is {name}"
