import asyncio
import os

import pytest
import pytest_mock
import vkquick as vq


@pytest.mark.asyncio
async def test_calling_command_via_payload(
    make_bot, make_message_new_event, mocker: pytest_mock.MockerFixture
):
    bot = make_bot()
    event = make_message_new_event()
    event.msg._fields["payload"] = '{"command":"foo","args":{"arg":1}}'

    def foo(ctx, arg: vq.Integer):
        ...

    mocked_reaction = mocker.create_autospec(foo)
    com = bot.add_command()(mocked_reaction)
    mocker.patch.object(com, "call_reaction")

    await bot.run_command_via_payload(event)

    com.call_reaction.assert_called_once()
    kwargs = com.call_reaction.call_args.kwargs
    assert kwargs["context"].extra.reaction_arguments.arg == 1
    com.call_reaction.reset_mock()

    event.msg._fields["payload"] = '{"command":"foo"}'
    await bot.run_command_via_payload(event)
    assert len(kwargs["context"].extra.reaction_arguments)


@pytest.mark.asyncio
async def test_pass_event_trough_commands(
    make_message_new_event, make_bot, mocker
):
    event = make_message_new_event()
    bot = make_bot()
    # LMAO naming
    mocked_shower = mocker.patch.object(bot, "show_debug_info")

    @bot.add_command(names="foo")
    def foo():
        ...

    event.msg._fields["text"] = "foo"
    await bot.pass_event_trough_commands(event)
    mocked_shower.assert_called_once()


async def _run_handling(bot, event):
    await bot.pass_event_trough_commands(event)
    bot._set_new_event(event)


@pytest.mark.asyncio
async def test_waiters(make_bot, make_message_new_event, mocker):
    os.environ["VKQUICK_RELEASE"] = "0"
    event1 = make_message_new_event()
    event1.msg._fields["peer_id"] = 1
    event1.msg._fields["from_id"] = 1
    event1.msg._fields["text"] = "a"

    event2 = make_message_new_event()
    event2.msg._fields["peer_id"] = 1
    event2.msg._fields["from_id"] = 1
    event2.msg._fields["text"] = "b"

    bot = make_bot()
    bot.shared_box.extra.command_called_completely = False
    mocked_shower = mocker.patch.object(bot, "show_debug_info")
    bot.shared_box.extra.mocked_shower = mocked_shower

    @bot.add_command(names="a")
    async def foo(ctx):
        new_ctx = await ctx.conquer_new_message(include_output_messages=True)
        if new_ctx.msg.text == "b":
            bot.shared_box.extra.command_called_completely = True

    await asyncio.gather(
        _run_handling(bot, event1), _run_handling(bot, event2)
    )

    assert bot.shared_box.extra.command_called_completely


def test_invalid_command(make_bot):
    bot = make_bot()

    with pytest.raises(TypeError):
        bot.add_command(1)

    com = vq.Command(names="a")
    bot.add_command(com)
    assert bot.commands == [com]


def test_run(make_bot, mocker):
    bot = make_bot()
    mocker.patch.object(bot, "async_run", side_effect=KeyboardInterrupt())
    bot.run()


def test_make_many_copies(make_bot, mocker):
    mocked_api = mocker.patch("vkquick.bot.API")
    bot = make_bot()
    mocked_api.side_effect = [
        vq.API("token1", token_owner="group"),
        vq.API("token2", token_owner="user"),
    ]
    bot.add_command(vq.Command())
    bot.add_command(vq.Command())
    bot.add_command(vq.Command())
    bot.add_signal_handler(vq.SignalHandler())
    bot._debugger = "123"
    tokens = ["token1", "token2"]
    bots = bot.make_many_copies(tokens)
    assert ["token", "token1", "token2"] == [
        bots[0].api.token,
        bots[1].api.token,
        bots[2].api.token,
    ]
    assert ["token", "token1", "token2"] == [
        bots[0].events_generator._api.token,
        bots[1].events_generator._api.token,
        bots[2].events_generator._api.token,
    ]
    assert bots[0].commands == bots[1].commands == bots[2].commands
    assert (
        bots[0]._signal_handlers
        == bots[1]._signal_handlers
        == bots[2]._signal_handlers
    )
    assert bots[0]._debugger == bots[1]._debugger == bots[2]._debugger
    assert bots[2].events_generator


def test_run_may_bots(mocker, make_bot):
    os.environ["VKQUICK_RELEASE"] = "0"
    mocked_bot = mocker.patch("vkquick.bot.Bot.async_run")
    bot = make_bot()
    mocked_api = mocker.patch("vkquick.bot.API")
    other_bot = bot.copy("new-token")
    vq.run_many_bots([bot, other_bot])
    assert mocked_bot.call_count == 2
    assert bot.release and other_bot.release
