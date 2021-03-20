import concurrent.futures

import pytest
import pytest_mock

import vkquick as vq


def test_raises_init():
    with pytest.raises(ValueError):
        vq.Command(run_in_thread=True, run_in_process=True)

    com = vq.Command(run_in_process=True)
    assert isinstance(com._pool, concurrent.futures.ProcessPoolExecutor)
    com = vq.Command(run_in_thread=True)
    assert isinstance(com._pool, concurrent.futures.ThreadPoolExecutor)

    async def foo():
        ...

    with pytest.raises(ValueError):
        com(foo)

    with pytest.raises(ValueError):
        vq.Command(names="a", any_text=True)


class TestFields:
    def test_title(self):
        com = vq.Command(title="a")
        assert com.title == "a"

    def test_description(self):
        com = vq.Command(description="a")
        assert com.description == "a"

        @vq.Command(description="a")
        def com():
            """
            description
            """

        assert com.description == "a"

        @vq.Command()
        def com():
            """
            description
            """

        assert com.description == "description"

        @vq.Command()
        def com():
            ...

        assert com.description == "Описание отсутствует"

    def test_reaction_arguments(self):
        @vq.Command()
        def com(
            arg: vq.Integer(),
            arg1: vq.Integer,
            arg2: int = vq.Integer,
            arg3: int = vq.Integer(),
        ):
            ...

        assert len(com.reaction_arguments) == 4
        for _, argtype in com.reaction_arguments:
            assert isinstance(argtype, vq.Integer)

        @vq.Command()
        def com(
            crx: vq.Context,
            arg: vq.Integer(),
            arg1: vq.Integer,
            arg2: int = vq.Integer,
            arg3: int = vq.Integer(),
        ):
            ...

        assert len(com.reaction_arguments) == 4
        for _, argtype in com.reaction_arguments:
            assert isinstance(argtype, vq.Integer)

    def test_extra(self):
        com = vq.Command(extra={"a": 1})
        assert com.extra() == {"a": 1}

    def test_reaction_context_argument_name(self):
        com = vq.Command(extra={"a": 1})(lambda x: ...)
        assert com.reaction_context_argument_name == "x"

    def test_payload_names(self):
        com = vq.Command(payload_names=("a",))
        assert com.payload_names == ("a",)

        @vq.Command()
        def foo():
            ...

        assert foo.payload_names == ("foo",)

    def test_prefixes(self):
        com = vq.Command(prefixes="/")
        assert com.prefixes == ("/",)
        com = vq.Command(prefixes=["/"])
        assert com.prefixes == ("/",)

    def test_names(self):
        com = vq.Command(names="a")
        assert com.names == ("a",)
        com = vq.Command(names=["a"])
        assert com.names == ("a",)

    def test_dynamic_routings(self):
        com = vq.Command(prefixes="/", names="a")
        assert com._command_routing_regex.pattern == "/a"
        com.names = "b"
        assert com._command_routing_regex.pattern == "/b"
        com.prefixes = "!"
        assert com._command_routing_regex.pattern == "!b"
        com.names = ["a", "b"]
        assert com._command_routing_regex.pattern == "!(?:a|b)"
        com.prefixes = ["/", "!"]
        assert com._command_routing_regex.pattern == "(?:/|!)(?:a|b)"

    def test_filters(self):
        any_filter = vq.ChatOnly()

        @any_filter
        @vq.Command()
        def com():
            ...

        assert com.filters == [com, any_filter]

    def test_human_style_args(self):
        assert vq.Command(
            human_style_arguments_name={"a": "b"}
        ).human_style_arguments_name == {"a": "b"}

    def test_invalid_argument_handlers_init(self):
        @vq.Command(on_invalid_argument={"arg1": "foo"})
        def com(arg1: vq.Integer, arg2: vq.Integer, arg3: vq.Integer):
            ...

        @com.on_invalid_argument
        def arg2():
            return "foo"

        @com.on_invalid_argument("arg3")
        def arg():
            return "foo"

        assert com.invalid_argument_handlers == {
            "arg1": "foo",
            "arg2": arg2,
            "arg3": arg,
        }

        with pytest.raises(KeyError):

            @com.on_invalid_argument
            def arg2(a, b):
                return "foo"

    def test_invalid_filter_init(self):
        @vq.DirectOnly()
        @vq.ChatOnly()
        @vq.Command(on_invalid_filter={vq.ChatOnly: "foo"})
        def com():
            ...

        @com.on_invalid_filter(vq.DirectOnly)
        def bar():
            ...

        assert com.invalid_filter_handlers == {
            vq.ChatOnly: "foo",
            vq.DirectOnly: bar,
        }

        with pytest.raises(KeyError):

            @com.on_invalid_filter(vq.DirectOnly)
            def bar(a, b):
                ...


def test_resolve_text_cutter():
    with pytest.raises(TypeError):

        @vq.Command()
        def com(ctx, arg):
            ...

    with pytest.raises(TypeError):

        @vq.Command()
        def com(ctx, arg: vq.Context):
            ...

    with pytest.raises(TypeError):

        @vq.Command()
        def com(ctx, arg: int):
            ...


def test_escaping():
    com = vq.Command(prefixes="?", names="?")
    assert com._command_routing_regex.pattern == "\?\?"
    com = vq.Command(prefixes="a?", names="a?", use_regex_escape=False)
    assert com._command_routing_regex.pattern == "a?a?"


@pytest.mark.asyncio
async def test_init_text_arguments():
    @vq.Command()
    def com(arg: vq.Integer, arg1: vq.Word):
        ...

    assert await com.init_text_arguments("123 abc", None) == (
        True,
        {"arg": 123, "arg1": "abc"},
    )

    @vq.Command()
    def com(ctx: vq.Context, arg: vq.Integer, arg1: vq.Word):
        ...

    assert await com.init_text_arguments("123 abc", None) == (
        True,
        {"arg": 123, "arg1": "abc"},
    )


@pytest.mark.asyncio
async def test_failed_init_text_arguments(mocker: pytest_mock.MockerFixture):

    arg1_type = vq.Word()
    mocker.patch.object(arg1_type, "invalid_value")

    @vq.Command()
    def com(arg: vq.Integer, arg1: arg1_type, arg2: vq.Integer):
        ...

    def arg_handler():
        ...

    arg_handler = mocker.create_autospec(arg_handler)
    arg_handler = com.on_invalid_argument("arg")(arg_handler)

    ctx = mocker.Mock()
    ctx.reply = mocker.AsyncMock()

    assert await com.init_text_arguments("123 abc 123", None) == (
        True,
        {"arg": 123, "arg1": "abc", "arg2": 123},
    )

    assert await com.init_text_arguments("abc abc", ctx) == (
        False,
        {"arg": vq.UnmatchedArgument},
    )
    arg_handler.assert_called_once()

    ctx.reply.reset_mock()

    assert await com.init_text_arguments("123 abc abc", ctx) == (
        False,
        {"arg": 123, "arg1": "abc", "arg2": vq.UnmatchedArgument},
    )
    ctx.reply.assert_called_once()

    assert await com.init_text_arguments("123 abc 123 123", ctx) == (
        False,
        {"arg": 123, "arg1": "abc", "arg2": 123},
    )
    assert await com.init_text_arguments("123 abc 123 123 123", ctx) == (
        False,
        {"arg": 123, "arg1": "abc", "arg2": 123},
    )

    @vq.Command(argline="1 {arg} 3")
    def com(arg: vq.Integer):
        ...

    assert await com.init_text_arguments("1 2 3", ctx) == (True, {"arg": 2},)


@pytest.mark.asyncio
async def test_calling_invalid_arguments_handlers(
    mocker: pytest_mock.MockerFixture,
):
    @vq.Command()
    def com(arg: vq.Integer):
        ...

    def arg_handler(ctx):
        ...

    arg_handler = mocker.create_autospec(arg_handler)
    arg_handler = com.on_invalid_argument("arg")(arg_handler)

    ctx = mocker.Mock()
    ctx.reply = mocker.AsyncMock()

    await com.init_text_arguments("abc", ctx)

    arg_handler.assert_called_once_with(ctx)
    ctx.reply.reset_mock()

    @vq.Command(on_invalid_argument={"arg": "123"})
    def com(arg: vq.Integer):
        ...

    await com.init_text_arguments("abc", ctx)

    ctx.reply.assert_called_once()


def test_make_reaction_arguments_via_argline():
    @vq.Command(argline=" 1 {arg} 2 {arg1} 3")
    def foo(arg: vq.Integer, arg1: vq.Word):
        ...

    assert foo._argline == "1 {arg} 2 {arg1} 3"
    assert (
        foo.reaction_arguments[0][0]
        == foo.reaction_arguments[2][0]
        == "__argline_regex_part"
        == foo.reaction_arguments[4][0]
    )
    assert foo.reaction_arguments[0][1].pattern.pattern == "1 "
    assert foo.reaction_arguments[2][1].pattern.pattern == " 2 "
    assert foo.reaction_arguments[4][1].pattern.pattern == " 3"

    with pytest.raises(KeyError):

        @vq.Command(argline="1 {arg} 2 {arg1} 3")
        def foo():
            ...


@pytest.mark.asyncio
async def test_run_through_filters(
    make_message_new_event, mocker: pytest_mock.MockerFixture
):
    @vq.ChatOnly()
    @vq.Command(names="a", on_invalid_filter={vq.ChatOnly: "a"})
    def foo():
        ...

    event = make_message_new_event()
    event.msg.__fields["peer_id"] = 1
    event.msg.__fields["text"] = "a"

    ctx = vq.Context(event=event, shared_box=None)
    ctx.reply = mocker.AsyncMock()

    result, decisions = await foo.run_through_filters(ctx)
    assert not result
    assert len(decisions) == 2
    ctx.reply.assert_called_once()

    event.msg.__fields["peer_id"] = vq.peer(1)

    result, decisions = await foo.run_through_filters(ctx)
    assert result
    assert len(decisions) == 2


@pytest.mark.asyncio
async def test_handle_event(make_message_new_event):
    event = make_message_new_event()
    event.msg.__fields["text"] = "a"

    @vq.Command(names="a")
    def foo():
        ...

    response = await foo.handle_event(event, None)
    assert response.all_filters_passed

    event.msg.__fields["text"] = "b"

    @vq.Command(names="a")
    def foo():
        ...

    response = await foo.handle_event(event, None)
    assert not response.all_filters_passed


@pytest.mark.asyncio
async def test_make_decision(
    make_message_new_event, mocker: pytest_mock.MockerFixture
):
    event = make_message_new_event()
    event.msg.__fields["text"] = "a"

    @vq.Command(any_text=True)
    def foo(ctx):
        ...

    ctx = vq.Context(event=event, shared_box=None)
    ctx.reply = mocker.AsyncMock()

    passed, _ = await foo.make_decision(context=ctx)
    assert ctx.extra.reaction_arguments == {"ctx": ctx}
    assert passed

    @vq.Command(names="a")
    def foo(arg: vq.Integer):
        ...

    passed, _ = await foo.make_decision(context=ctx)
    assert not passed

    @vq.Command(names="a")
    def foo():
        ...

    event.msg.__fields["text"] = "a a"

    passed, _ = await foo.make_decision(context=ctx)
    assert not passed

    @vq.Command(names="a")
    def foo(arg: vq.Word):
        ...

    event.msg.__fields["text"] = "aa"

    passed, _ = await foo.make_decision(context=ctx)
    assert not passed

    @vq.Command(names="a")
    def foo(arg: vq.Word):
        ...

    event.msg.__fields["text"] = "a a"

    passed, _ = await foo.make_decision(context=ctx)
    assert passed


def test_str():
    @vq.Command(names="foo", prefixes="/")
    def foo():
        ...

    assert (
        str(foo) == "<Command title='foo', prefixes=('/',), names=('foo',)>"
    )


@pytest.mark.asyncio
async def test_call_reaction(mocker: pytest_mock.MockerFixture):
    ctx = vq.Context(event=None, shared_box=None)
    ctx.reply = mocker.AsyncMock()
    ctx.extra.reaction_arguments = {}

    @vq.Command(any_text=True)
    def foo():
        return "ok"

    await foo.call_reaction(ctx)
    ctx.reply.assert_called_once_with("ok")

    @vq.Command(any_text=True, run_in_thread=True)
    def foo():
        return "ok"

    await foo.call_reaction(ctx)
