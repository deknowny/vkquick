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