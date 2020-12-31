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
    (vq.Integer(max_=10), "5", 5),
    (vq.Integer(max_=10), "15", vq.UnmatchedArgument),
    (vq.Word(), "hello", "hello"),
    (vq.Word(), "hello_world", "hello_world"),
    (vq.Word(), "hello world", "hello"),
    (vq.Word(), "123hello123", "123hello123"),
    (vq.Word(), "123 123", "123"),
    (vq.Word(), "123,", "123"),
    (vq.Word(), ",123", vq.UnmatchedArgument),
    (vq.Word(min_length=10), "a" * 15, "a" * 15),
    (vq.Word(min_length=10), "a" * 5, vq.UnmatchedArgument),
    (vq.Word(max_length=10), "a" * 5, "a" * 5),
    (vq.Word(max_length=10), "a" * 15, vq.UnmatchedArgument),
    (vq.Word(min_length=10, max_length=20), "a" * 15, "a" * 15),
    (vq.Word(min_length=10, max_length=20), "a" * 5, vq.UnmatchedArgument),
    (vq.Word(min_length=10, max_length=20), "a" * 25, vq.UnmatchedArgument),
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
    (vq.String(dotall=False), "\n\n", vq.UnmatchedArgument),
    (vq.String(dotall=False), "1\n2", "1"),
    (vq.Union(vq.Integer(), vq.Word()), "123", 123),
    (vq.Union(vq.Word(), vq.Integer()), "123", "123"),
    (vq.Union(vq.Integer(), vq.Word()), "abc", "abc"),
    (vq.Union(vq.Integer(), vq.Word()), "abc cde", "abc"),
    (vq.Union(vq.Word(), vq.String()), "abc cde", "abc"),
    (vq.Union(vq.Word(), vq.String()), ",abc cde", ",abc cde"),
    (
        vq.Union(vq.Integer(max_=10), vq.Integer(min_=20, max_=30)),
        "15",
        vq.UnmatchedArgument,
    ),
    (vq.Regex(regex="hello", factory=lambda x: x.group(0)), "hello", "hello"),
    (
        vq.Regex(regex=re.compile("hello"), factory=lambda x: x.group(0)),
        "hello",
        "hello",
    ),
    (
        vq.Regex(
            regex=r"(?P<group>\d+)", factory=lambda x: int(x.group("group"))
        ),
        "123",
        123,
    ),
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
    (vq.Bool(), "on,", True),
    (vq.Bool(), "?", vq.UnmatchedArgument),
    (vq.List(vq.Integer()), "123 123 123", [123, 123, 123]),
    (vq.List(vq.Integer()), "123,123, 123", [123, 123, 123]),
    (vq.List(vq.Integer(), min_length=2), "123", vq.UnmatchedArgument),
    (vq.List(vq.Integer(), max_length=2), "123 123 123 123", [123, 123]),
    (
        vq.List(vq.Union(vq.Integer(), vq.Word())),
        "123 abc 123 dec",
        [123, "abc", 123, "dec"],
    ),
    (vq.Optional(vq.Integer()), "123", 123),
    (vq.Optional(vq.Integer()), "abc", None),
    (vq.Optional(vq.Integer(), default=123), "abc", 123),
    (vq.Optional(vq.Integer(), default_factory=dict), "abc", {}),
    (vq.UserMention(), "[id123|Tom]", 123),
    (vq.GroupMention(), "[club123|vk]", 123),
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


class TestRaises:
    def test_union_raises(self):
        with pytest.raises(ValueError):
            vq.Union()

        with pytest.warns(UserWarning):
            vq.Union(vq.Integer())

    def test_integer_raises(self):
        with pytest.raises(ValueError):
            vq.Integer(min_=10, max_=5)


usages_description = [
    (vq.Integer(), "Аргумент должен быть целым числом."),
    (
        vq.Integer(min_=10),
        "Аргумент должен быть целым числом. Минимальное значение 10.",
    ),
    (
        vq.Integer(max_=10),
        "Аргумент должен быть целым числом. Максимальное значение 10.",
    ),
    (
        vq.Integer(min_=5, max_=10),
        "Аргумент должен быть целым числом. Минимальное значение 5. Максимальное значение 10.",
    ),
    (vq.Regex("123123"), "Аргумент должен подходить под шаблон 123123."),
    (
        vq.Bool(),
        "Аргумент является булевым значением (да/нет, +/-, on/off...).",
    ),
    (vq.UserMention(), "Аргумент является упоминанием пользователя.",),
    (vq.GroupMention(), "Аргумент является упоминанием группы.",),
    (
        vq.String(),
        "Аргумент является строкой, содержащей любые символы. "
        "Минимальная длина строки больше или равна 1, а максимальная не ограничена.",
    ),
    (
        vq.String(dotall=False),
        "Аргумент является строкой, содержащей любые символы, кроме новой строки. "
        "Минимальная длина строки больше или равна 1, а максимальная не ограничена.",
    ),
    (
        vq.List(vq.Integer()),
        vq.Integer().usage_description()
        + " Минимальное количество подобных аргументов больше или равно 1, "
        "а максимальное не ограничено.",
    ),
    (
        vq.List(vq.Integer(), max_length=10),
        vq.Integer().usage_description()
        + " Минимальное количество подобных аргументов больше или равно 1, "
        "а максимальное меньше или равно 10.",
    ),
    (
        vq.Optional(vq.Integer()),
        vq.Integer().usage_description()
        + " Передаваемое значение может быть полностью пропущено.",
    ),
    (
        vq.Union(vq.UserMention(), vq.GroupMention()),
        "Значение должно подходить под одно из следующих описаний:\n"
        f"1) {vq.UserMention().usage_description()}\n"
        f"2) {vq.GroupMention().usage_description()}",
    ),
    (
        vq.Word(),
        "Аргумент может состоять из букв, чисел или знака нижнего подчеркивания. "
        "Минимальная длина строки больше или равна 1, а максимальная не ограничена.",
    ),
    (
        vq.Word(max_length=10),
        "Аргумент может состоять из букв, чисел или знака нижнего подчеркивания. "
        "Минимальная длина строки больше или равна 1, а максимальная меньше или равна 10.",
    ),
]


@pytest.mark.parametrize("cutter,output", usages_description)
def test_usage_description(cutter, output):
    assert cutter.usage_description() == output


def test_text_base():
    with pytest.raises(ValueError):
        vq.TextBase.check_valid_length(max_length=-5, min_length=1)
    with pytest.raises(ValueError):
        vq.TextBase.check_valid_length(max_length=10, min_length=20)
    with pytest.raises(ValueError):
        vq.TextBase.check_valid_length(max_length=10, min_length=-2)
    with pytest.raises(ValueError):
        vq.TextBase.check_valid_length(max_length=-5, min_length=-10)
