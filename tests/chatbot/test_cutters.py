import asyncio
import typing
import unittest.mock

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
                vq.IntegerCutter(), vq.LiteralCutter(r"\s+"), vq.WordCutter()
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
        (
            vq.MutableSequenceCutter(vq.IntegerCutter()),
            "123,456 678 , 901",
            [123, 456, 678, 901],
        ),
        (
            vq.ImmutableSequenceCutter(
                vq.UnionCutter(vq.IntegerCutter(), vq.WordCutter())
            ),
            "123,456 abc , 901",
            (123, 456, "abc", 901),
        ),
        (
            vq.UniqueMutableSequenceCutter(
                vq.UnionCutter(vq.IntegerCutter(), vq.WordCutter())
            ),
            "",
            set(),
        ),
        (
            vq.UniqueImmutableSequenceCutter(vq.IntegerCutter()),
            "123 abc",
            frozenset([123]),
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


@pytest.mark.asyncio
async def test_mention_with_wrapper(group_api):
    mocked_context = unittest.mock.Mock()
    mocked_context.api = group_api

    cutter = vq.MentionCutter(vq.Page)
    call1 = await cutter.cut_part(mocked_context, "[id1|abc]")
    call2 = await cutter.cut_part(mocked_context, "[club1|abc]")
    assert call1.parsed_part.alias == call2.parsed_part.alias == "abc"
    assert call1.parsed_part.entity.id == call2.parsed_part.entity.id == 1
    assert isinstance(call1.parsed_part.entity, vq.User)
    assert isinstance(call2.parsed_part.entity, vq.Group)

    cutter = vq.MentionCutter(vq.Group)
    with pytest.raises(vq.BadArgumentError):
        await cutter.cut_part(mocked_context, "[id1|abc]")
    call = await cutter.cut_part(mocked_context, "[club1|abc]")
    assert call.parsed_part.alias == "abc"
    assert call.parsed_part.entity.id == 1
    assert isinstance(call.parsed_part.entity, vq.Group)

    cutter = vq.MentionCutter(vq.User)
    with pytest.raises(vq.BadArgumentError):
        await cutter.cut_part(mocked_context, "[club1|abc]")
    call = await cutter.cut_part(mocked_context, "[id1|abc]")
    assert call.parsed_part.alias == "abc"
    assert call.parsed_part.entity.id == 1
    assert isinstance(call.parsed_part.entity, vq.User)

    # Несуществующий ID
    with pytest.raises(vq.BadArgumentError):
        await cutter.cut_part(
            mocked_context, "[id123123123123123123123123|abc]"
        )

    cutter = vq.MentionCutter(vq.User[typing.Literal["bdate"]])
    call = await cutter.cut_part(mocked_context, "[id1|abc]")
    assert "bdate" in call.parsed_part.entity.fields


@pytest.mark.asyncio
async def test_mention_with_id():
    cutter = vq.MentionCutter(vq.PageID)
    call1 = await cutter.cut_part(None, "[id123|abc]")
    call2 = await cutter.cut_part(None, "[club123|abc]")
    assert call1.parsed_part.alias == call2.parsed_part.alias == "abc"
    assert call1.parsed_part.entity == call2.parsed_part.entity == 123
    assert call1.parsed_part.page_type == vq.PageType.USER
    assert call2.parsed_part.page_type == vq.PageType.GROUP

    cutter = vq.MentionCutter(vq.GroupID)
    with pytest.raises(vq.BadArgumentError):
        await cutter.cut_part(None, "[id123|abc]")
    call = await cutter.cut_part(None, "[club123|abc]")
    assert call.parsed_part.alias == "abc"
    assert call.parsed_part.entity == 123
    assert call.parsed_part.page_type == vq.PageType.GROUP

    cutter = vq.MentionCutter(vq.UserID)
    with pytest.raises(vq.BadArgumentError):
        await cutter.cut_part(None, "[club123|abc]")
    call = await cutter.cut_part(None, "[id123|abc]")
    assert call.parsed_part.alias == "abc"
    assert call.parsed_part.entity == 123
    assert call.parsed_part.page_type == vq.PageType.USER


@pytest.mark.parametrize(
    "input_string",
    [
        "[id1|abc]",
        "vk.com/durov",
        "vk.com/id1",
        "https://vk.com/id1",
        "http://vk.com/id1",
        "id1",
        "durov",
        "1",
    ],
)
@pytest.mark.asyncio
async def test_group_entity_by_string(input_string, group_api):
    mocked_context = unittest.mock.Mock()
    mocked_context.api = group_api
    page_cutter = vq.EntityCutter(vq.Page)
    user_cutter = vq.EntityCutter(vq.User)
    user_id_cutter = vq.EntityCutter(vq.User)
    result_page, result_user, result_user_id = await asyncio.gather(
        page_cutter.cut_part(mocked_context, input_string),
        user_cutter.cut_part(mocked_context, input_string),
        user_id_cutter.cut_part(mocked_context, input_string),
    )
    assert (
        result_page.parsed_part.id
        == result_user.parsed_part.id
        == result_user_id.parsed_part.id
        == 1
    )
