import asyncio
import os

import vkquick as vq
import pytest
import pytest_mock

import unittest.mock


def test_event_handler(
    attach_events,
    make_message_new_event,
    make_bot,
    mocker: pytest_mock.MockerFixture,
):
    os.environ["VKQUICK_RELEASE"] = "1"
    bot = make_bot()
    message_new = make_message_new_event()
    wall_post_new = make_message_new_event()
    wall_post_new["type"] = "wall_post_new"
    attach_events(bot, [message_new, wall_post_new])

    def message_new(event):
        ...

    message_new = mocker.create_autospec(message_new)
    message_new.__name__ = "message_new"
    message_new = bot.add_event_handler(message_new)

    def wall_post_new():
        ...

    wall_post_new = mocker.create_autospec(wall_post_new)
    wall_post_new.__name__ = "wall_post_new"
    wall_post_new = vq.EventHandler(wall_post_new)
    wall_post_new = bot.add_event_handler(wall_post_new)

    bot.run()

    message_new.handler.assert_called_once_with(mocker.ANY)
    wall_post_new.handler.assert_called_once_with()


def test_raises():
    with pytest.raises(ValueError):
        vq.EventHandler(handle_every_event=True, extra_types="1")

    with pytest.raises(TypeError):
        vq.EventHandler(lambda x, y: ...)
