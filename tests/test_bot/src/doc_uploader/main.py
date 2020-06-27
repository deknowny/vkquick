import pathlib
import vkquick as vq

from . import config
from tests.test_bot.src._add_cache import cache


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
async def doc_uploader(event: vq.Event()):
    """
    Handler to command `send_photo`
    """
    path = pathlib.Path() / "tests" / "test_bot" / "assets" / "example.png"
    with open(path, "rb") as file:
        photo_bytes = file.read()

    docs = await vq.Doc.message(
        file=photo_bytes,
        peer_id=event.object.message.peer_id,
        type_="doc"
    )()

    cache("doc_uploader")
    return vq.Message(attachment=docs)
