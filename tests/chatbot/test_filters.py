import unittest.mock

import pytest

import vkquick as vq


@pytest.mark.asyncio
async def test_and_filter():
    filter = vq.filters.OnlyMe() & vq.filters.IgnoreBots()
    mock = unittest.mock.Mock()
    mock.msg = unittest.mock.Mock()
    mock.msg.from_id = 100
    mock.msg.out = True

    await filter.make_decision(mock)

    mock.msg.out = False
    with pytest.raises(vq.FilterFailedError):
        await filter.make_decision(mock)

    mock.msg.out = True
    mock.msg.from_id = -100
    with pytest.raises(vq.FilterFailedError):
        await filter.make_decision(mock)


@pytest.mark.asyncio
async def test_or_filter():
    filter = vq.filters.OnlyMe() | vq.filters.IgnoreBots()
    mock = unittest.mock.Mock()
    mock.msg = unittest.mock.Mock()
    mock.msg.from_id = 100
    mock.msg.out = True

    await filter.make_decision(mock)

    mock.msg.out = False
    await filter.make_decision(mock)

    mock.msg.out = True
    mock.msg.from_id = -100
    await filter.make_decision(mock)

    mock.msg.out = False
    with pytest.raises(vq.FilterFailedError):
        await filter.make_decision(mock)


@pytest.mark.parametrize(
    "filter,fields,passed",
    [
        (vq.filters.OnlyMe(), {"out": True}, True),
        (vq.filters.OnlyMe(), {"out": False}, False),
        (vq.filters.IgnoreBots(), {"from_id": 100}, True),
        (vq.filters.IgnoreBots(), {"from_id": -100}, False),
        (vq.filters.ChatOnly(), {"peer_id": vq.peer(100)}, True),
        (vq.filters.ChatOnly(), {"peer_id": 100}, False),
        (vq.filters.DirectOnly(), {"peer_id": 100}, True),
        (vq.filters.DirectOnly(), {"peer_id": vq.peer(100)}, False),
        (
            vq.filters.Dynamic(lambda ctx: ctx.msg.some_field == "egg"),
            {"some_field": "egg"},
            True,
        ),
        (
            vq.filters.Dynamic(lambda ctx: 5 > 10),
            {"some_field": "egg"},
            False,
        ),
        (vq.filters.DirectOnly(), {"peer_id": vq.peer(100)}, False),
    ],
)
@pytest.mark.asyncio
async def test_or_filter(filter, fields, passed):
    mock = unittest.mock.Mock()
    mock.msg = unittest.mock.Mock()
    mock.msg.__dict__.update(fields)

    if passed:
        await filter.make_decision(mock)
    else:
        with pytest.raises(vq.FilterFailedError):
            await filter.make_decision(mock)
