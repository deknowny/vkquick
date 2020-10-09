import re

import pytest
import vkquick as vq


text_arguments_data = [
    (vq.Integer(), "123", 123),
    (vq.Integer(), "0", 0),
    (vq.Integer(), "823123000", 823123000),
    (vq.Integer(), "000", 0),
    (vq.Integer(), "123123a12123", 123123),
    (vq.Integer(), "a12123", vq.UnmatchedArgument),
    (vq.Integer(), "123 123", 123),
    (vq.Integer(range_=range(10)), "5", 5),
    (vq.Integer(range_=range(10)), "15", vq.UnmatchedArgument),

    (vq.Word(), "hello", "hello"),
    (vq.Word(), "hello_world", "hello_world"),
    (vq.Word(), "hello world", "hello"),
    (vq.Word(), "123hello123", "123hello123"),
    (vq.Word(), "123 123", "123"),
    (vq.Word(), "123,", "123"),
    (vq.Word(), ",123", vq.UnmatchedArgument),
    (vq.Word(min_length=10), "a"*15, "a"*15),
    (vq.Word(min_length=10), "a"*5, vq.UnmatchedArgument),
    (vq.Word(max_length=10), "a"*5, "a"*5),
    (vq.Word(max_length=10), "a"*15, vq.UnmatchedArgument),
    (vq.Word(min_length=10, max_length=20), "a"*15, "a"*15),
    (vq.Word(min_length=10, max_length=20), "a"*5, vq.UnmatchedArgument),
    (vq.Word(min_length=10, max_length=20), "a"*25, vq.UnmatchedArgument),

    (vq.String(), "abc def \n\n", "abc def \n\n"),
    (vq.String(), "", vq.UnmatchedArgument),
    (vq.String(), "\u1231\u4564", "\u1231\u4564"),
    (vq.String(min_length=10), "a" * 15, "a" * 15),
    (vq.String(min_length=10), "a" * 5, vq.UnmatchedArgument),
    (vq.String(max_length=10), "a" * 5, "a" * 5),
    (vq.String(max_length=10), "a" * 15, vq.UnmatchedArgument),
    (vq.String(min_length=10, max_length=20), "a" * 15, "a" * 15),
    (vq.String(min_length=10, max_length=20), "a" * 5, vq.UnmatchedArgument),
    (vq.String(min_length=10, max_length=20), "a" * 25, vq.UnmatchedArgument),

    (vq.Union(vq.Integer(), vq.Word()), "123", 123),
    (vq.Union(vq.Word(), vq.Integer()), "123", "123"),
    (vq.Union(vq.Integer(), vq.Word()), "abc", "abc"),
    (vq.Union(vq.Integer(), vq.Word()), "abc cde", "abc"),
    (vq.Union(vq.Word(), vq.String()), "abc cde", "abc"),
    (vq.Union(vq.Word(), vq.String()), ",abc cde", ",abc cde"),
    (vq.Union(vq.Integer(range_=range(10)), vq.Integer(range_=range(20, 30))), "15", vq.UnmatchedArgument),

    (vq.Regex(regex="hello", factory=lambda x: x.group(0)), "hello", "hello"),
    (vq.Regex(regex=re.compile("hello"), factory=lambda x: x.group(0)), "hello", "hello"),
    (vq.Regex(regex=r"(?P<group>\d+)", factory=lambda x: int(x.group("group"))), "123", 123),

    (vq.Bool(), "true", True),
    (vq.Bool(), "1", True),
    (vq.Bool(), "yes", True),
    (vq.Bool(), "y", True),
    (vq.Bool(), "да", True),
    (vq.Bool(), "д", True),
    (vq.Bool(), "истина", True),
    (vq.Bool(), "+", True),
    (vq.Bool(), "правда", True),
    (vq.Bool(), "t", True),
    (vq.Bool(), "on", True),
    (vq.Bool(), "вкл", True),
    (vq.Bool(), "enable", True),
    (vq.Bool(true_extension=["custom"]), "custom", True),

    (vq.Bool(), "false", False),
    (vq.Bool(), "0", False),
    (vq.Bool(), "no", False),
    (vq.Bool(), "n", False),
    (vq.Bool(), "нет", False),
    (vq.Bool(), "н", False),
    (vq.Bool(), "ложь", False),
    (vq.Bool(), "-", False),
    (vq.Bool(), "неправда", False),
    (vq.Bool(), "f", False),
    (vq.Bool(), "off", False),
    (vq.Bool(), "выкл", False),
    (vq.Bool(), "disable", False),
    (vq.Bool(false_extension=["custom"]), "custom", False),

    (vq.Bool(), "off,", False),
    (vq.Bool(), "on,", True)
]


@pytest.mark.parametrize(
    "instance,arguments_string,output_value", text_arguments_data
)
@pytest.mark.asyncio
async def test_cutting(instance, arguments_string, output_value):
    got_value, _ = await vq.sync_async_run(
        instance.cut_part(arguments_string)
    )
    assert got_value == output_value


def test_text_argument_union():
    with pytest.raises(ValueError):
        vq.Union()

    with pytest.warns(UserWarning):
        vq.Union(vq.Integer())


def test_text_base():
    with pytest.raises(ValueError):
        vq.TextBase.check_valid_length(max_length=-5, min_length=1)
    with pytest.raises(ValueError):
        vq.TextBase.check_valid_length(max_length=10, min_length=20)
    with pytest.raises(ValueError):
        vq.TextBase.check_valid_length(max_length=10, min_length=-2)