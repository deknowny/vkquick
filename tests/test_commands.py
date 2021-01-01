import concurrent.futures

import vkquick as vq
import pytest
import pytest_mock


def test_raises_init():
    with pytest.raises(ValueError):
        vq.Command(run_in_thread=True, run_in_process=True)

    com = vq.Command(run_in_process=True)
    assert isinstance(com._pool, concurrent.futures.ProcessPoolExecutor)
    com = vq.Command(run_in_thread=True)
    assert isinstance(com._pool, concurrent.futures.ThreadPoolExecutor)

    async def foo(): ...

    with pytest.raises(ValueError):
        com(foo)


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
            arg3: int = vq.Integer()
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
            arg3: int = vq.Integer()
        ):
            ...

        assert len(com.reaction_arguments) == 4
        for _, argtype in com.reaction_arguments:
            assert isinstance(argtype, vq.Integer)

    def test_extra(self):
        com = vq.Command(extra={"a": 1})
        assert com.extra() == {"a": 1}

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
        assert vq.Command(human_style_arguments_name={"a": "b"}).human_style_arguments_name == {"a": "b"}

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

        assert com.invalid_argument_handlers == {"arg1": "foo", "arg2": arg2, "arg3": arg}

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

        assert com.invalid_filter_handlers == {vq.ChatOnly: "foo", vq.DirectOnly: bar}

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