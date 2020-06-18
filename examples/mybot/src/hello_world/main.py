import vkquick as vq

from . import config


@vq.Cmd(prefs=["/"], names=["hello"])
@vq.Reaction("message_new")
def hello_world(users: [vq.UserMention()]):
    yield "Передаю привет:\n"
    for pos, user in enumerate(users, 1):
        yield f"{user:{pos}) <name>+<lname>}\n"
