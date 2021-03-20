import pytest
import pytest_mock

import vkquick as vq
import vkquick.context


@pytest.mark.asyncio
async def test_edit(mocker: pytest_mock.MockerFixture):
    api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
    mocked_method = mocker.patch.object(
        api, "method", new_callable=mocker.AsyncMock
    )
    sb = vq.SharedBox(api=api, events_generator=None, bot=None)

    mocked_context = mocker.patch("vkquick.Context.msg")
    mocked_context.out = True
    ctx = vq.Context(event=None, shared_box=sb)
    await ctx.edit("foo")
    args = mocked_method.call_args.args
    assert args[1]["message"] == "foo"
    assert args[0] == "messages.edit"

    mocked_context.out = True
    mocked_context.cmid = 1
    mocked_context.id = 0
    ctx = vq.Context(event=None, shared_box=sb)

    await ctx.edit("foo")
    args = mocked_method.call_args.args
    assert args[1]["message"] == "foo"
    assert args[0] == "messages.edit"

    mocked_context.out = False

    with pytest.raises(AssertionError):
        ctx = vq.Context(event=None, shared_box=sb)
        await ctx.edit("foo")


def test_exclude_content_source():
    ctx = vq.Context(None, None)
    assert ctx._auto_set_content_source
    ctx.exclude_content_source()
    assert not ctx._auto_set_content_source


@pytest.mark.asyncio
async def test_delete(mocker: pytest_mock.MockerFixture):
    api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
    mocked_method = mocker.patch.object(
        api, "method", new_callable=mocker.AsyncMock
    )
    sb = vq.SharedBox(api=api, events_generator=None, bot=None)

    mocked_context = mocker.patch("vkquick.Context.msg")
    mocked_context.out = True
    ctx = vq.Context(event=None, shared_box=sb)
    await ctx.delete()
    args = mocked_method.call_args.args
    assert args[0] == "messages.delete"


def test_str():
    ctx = vq.Context(None, None)
    assert str(ctx) == "Context(event, filters_response, extra, shared_box)"


@pytest.mark.asyncio
async def test_upload_doc(mocker: pytest_mock.MockerFixture):
    mocked_uploader = mocker.patch("vkquick.context.upload_doc_to_message")
    api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
    sb = vq.SharedBox(api=api, events_generator=None, bot=None)
    mocked_context = mocker.patch("vkquick.Context.msg")
    mocked_context.peer_id = vq.peer(1)
    ctx = vq.Context(event=None, shared_box=sb)
    await ctx.upload_doc(filepath="a")
    mocked_uploader.assert_called_once()


@pytest.mark.asyncio
async def test_answer(mocker: pytest_mock.MockerFixture):
    message = vq.AttrDict(
        [{"peer_id": 1, "message_id": 1, "conversation_message_id": 1}]
    )
    api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
    lp = api.init_group_lp()
    mocked_method = mocker.patch.object(
        api, "method", new_callable=mocker.AsyncMock, return_value=message
    )
    lp._group_id = 1
    sb = vq.SharedBox(api=api, events_generator=lp, bot=None)
    mocked_context = mocker.patch("vkquick.Context.msg")
    mocked_context.peer_id = 1
    mocked_context.message_id = 1
    mocked_context.conversation_message_id = 1

    ctx = vq.Context(event=None, shared_box=sb)
    await ctx.answer("abc")
    args = mocked_method.call_args.args
    assert args[0] == "messages.send"
    assert args[1]["message"] == "abc"
    assert args[1]["peer_ids"] == 1
    assert isinstance(args[1]["random_id"], int)
    assert args[1]["content_source"] is not None
