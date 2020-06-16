import vkquick as vq

from . import config


@vq.Cmd(
    prefs=["/"],
    names=["hello"]
)
@vq.Reaction("message_new")
def hello_world(some: int, foo: [vq.Word]):
    return f"{some=}, {foo=}"
