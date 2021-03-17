import typing as ty
import unittest.mock

import pytest

import vkquick as vq


@pytest.fixture(scope="session")
def make_bot() -> ty.Callable[[], vq.Bot]:
    def wrapper():
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        lp = api.init_group_lp()
        bot = vq.Bot(api=api, events_generator=lp)
        return bot

    return wrapper


@pytest.fixture(scope="session")
def make_message_new_event():
    def wrapper():
        event_scheme = {
            "type": "message_new",
            "object": {
                "message": {
                    "date": 1609512859,
                    "from_id": 447532348,
                    "id": 5236,
                    "out": 0,
                    "peer_id": 447532348,
                    "text": "hi",
                    "conversation_message_id": 4945,
                    "fwd_messages": [],
                    "important": False,
                    "random_id": 0,
                    "attachments": [],
                    "is_hidden": False,
                },
                "client_info": {
                    "button_actions": [
                        "text",
                        "intent_subscribe",
                        "intent_unsubscribe",
                    ],
                    "keyboard": True,
                    "inline_keyboard": False,
                    "carousel": False,
                    "lang_id": 0,
                },
            },
            "group_id": 192979547,
            "event_id": "f6277d86eb8c3f1c580cf7991fe29979b8afe3d2",
        }
        event = vq.Event(event_scheme)
        return event

    return wrapper


@pytest.fixture(scope="session")
def attach_events():
    def wrapper(bot, events):
        async def pull_new_events(events):
            yield events

        eg_mock = unittest.mock.Mock()
        puller = pull_new_events(events)
        eg_mock.__aiter__ = unittest.mock.Mock(
            return_value=puller.__aiter__()
        )
        eg_mock.__anext__ = unittest.mock.AsyncMock(
            return_value=puller.__anext__
        )
        eg_mock.close_session = unittest.mock.AsyncMock()
        eg_mock._setup = unittest.mock.AsyncMock()
        bot.shared_box.events_generator = eg_mock

    return wrapper
