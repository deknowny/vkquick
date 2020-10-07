import pathlib
import vkquick as vq

from . import config
from tests.test_bot.src._add_cache import cache


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
async def send_photo(event: vq.Event()):
    """
    Handler to command `send_photo`
    """
    path = pathlib.Path() / "tests_old" / "test_bot" / "assets" / "example.png"
    with open(path, "rb") as file:
        photo_bytes = file.read()

    photos = await vq.Photo.message(
        path,
        photo_bytes,
        pathlib.Path() / "tests_old" / "test_bot" / "assets" / "example2.jpg",
        pathlib.Path() / "tests_old" / "test_bot" / "assets" / "example2.jpg",
        pathlib.Path() / "tests_old" / "test_bot" / "assets" / "example2.jpg",
        path,
        await vq.Photo.download(
            "https://www.prikol.ru/wp-content/gallery/october-2019/prikol-25102019-001.jpg"
        ),
        pathlib.Path() / "tests_old" / "test_bot" / "assets" / "example2.jpg",
        pathlib.Path() / "tests_old" / "test_bot" / "assets" / "example2.jpg",
        pathlib.Path() / "tests_old" / "test_bot" / "assets" / "example2.jpg",
        peer_id=event.object.message.peer_id
    )()

    cache("send_photo")
    return vq.Message(attachment=photos)
