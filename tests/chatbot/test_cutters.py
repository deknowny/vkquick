import pytest
import vkquick as vq


NOT_PARSED = object()


@pytest.mark.parametrize(
    "cutter,string,expected",
    [
        (vq.IntegerCutter(), "123", 123),
        (vq.IntegerCutter(), "123 456", 123),
        (vq.IntegerCutter(), "007", 7),
        (vq.IntegerCutter(), "1b2", 1),
        (vq.IntegerCutter(), "+12", 12),
        (vq.IntegerCutter(), "-12", -12),
        (vq.IntegerCutter(), "abc2", NOT_PARSED),
        (vq.FloatCutter(), "12.1", 12.1),
        (vq.FloatCutter(), ".1", 0.1),
        (vq.FloatCutter(), "+12.1", 12.1),
        (vq.FloatCutter(), "-.1", -0.1),
        (vq.FloatCutter(), "12e5", 12e5),
        (vq.FloatCutter(), "12E-5", 12e-5),
        (vq.FloatCutter(), "-12E-5", -12e-5),
        (vq.FloatCutter(), "~12E-5", NOT_PARSED),
        (vq.WordCutter(), "foobar", "foobar"),
        (vq.WordCutter(), "foo123", "foo123"),
        (vq.WordCutter(), "!@привет#4123", "!@привет#4123"),
        (vq.WordCutter(), "foo bar", "foo"),
        (vq.WordCutter(), "\nfoo bar", NOT_PARSED),
        (
            vq.StringCutter(),
            "!@привет#4123\n\n !@привет#4123",
            "!@привет#4123\n\n !@привет#4123",
        ),
        (
            vq.ParagraphCutter(),
            "!@привет#4123 !@привет#4123",
            "!@привет#4123 !@привет#4123",
        ),
        (
            vq.ParagraphCutter(),
            "!@привет#4123\n!@привет#4123",
            "!@привет#4123",
        ),
        (vq.OptionalCutter(vq.IntegerCutter()), "123", 123),
        (vq.OptionalCutter(vq.IntegerCutter()), "abc", None),
        (vq.OptionalCutter(vq.IntegerCutter(), default=123), "abc", 123),
        (
            vq.OptionalCutter(vq.IntegerCutter(), default_factory=int),
            "abc",
            0,
        ),
        (vq.UnionCutter(vq.IntegerCutter(), vq.WordCutter()), "abc", "abc"),
        (vq.UnionCutter(vq.IntegerCutter(), vq.WordCutter()), "123", 123),
        (
            vq.OptionalCutter(
                vq.UnionCutter(vq.IntegerCutter(), vq.WordCutter())
            ),
            " ",
            None,
        ),
        (
            vq.GroupCutter(vq.IntegerCutter(), vq.WordCutter()),
            "123",
            NOT_PARSED,
        ),
        (
            vq.GroupCutter(vq.IntegerCutter(), vq.WordCutter()),
            "123abc",
            (123, "abc"),
        ),
        (
            vq.GroupCutter(
                vq.IntegerCutter(), vq.LiteralCutter("\s+"), vq.WordCutter()
            ),
            "123   abc",
            (123, "   ", "abc"),
        ),
        (
            vq.GroupCutter(
                vq.IntegerCutter(), vq.LiteralCutter("!"), vq.WordCutter()
            ),
            "123abc",
            NOT_PARSED,
        ),
    ],
)
@pytest.mark.asyncio
async def test_simple_cutters(cutter, string, expected):
    try:
        parsed_result = await cutter.cut_part(None, string)
    except vq.BadArgumentError:
        assert expected is NOT_PARSED
    else:
        assert parsed_result.parsed_part == expected
