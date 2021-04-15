import dataclasses
import re
import typing as ty

from vkquick.ext.chatbot.providers.page import UserProvider, GroupProvider, PageProvider
from vkquick.ext.chatbot.wrappers.page import User, Group, Page
from vkquick.ext.chatbot.command.context import Context
from vkquick.ext.chatbot.command.text_cutters.base import (
    CutterParsingResponse,
    TextCutter,
    cut_part_via_regex,
)
from vkquick.ext.chatbot.exceptions import BadArgumentError


T = ty.TypeVar("T")


class IntegerCutter(TextCutter):

    _pattern = re.compile(r"([+|-]?\d+)")

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        return cut_part_via_regex(
            self._pattern, arguments_string, factory=int
        )


class FloatCutter(TextCutter):

    _pattern = re.compile(r"([+|-]?\d*(?:\.?\d+))")

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        return cut_part_via_regex(
            self._pattern, arguments_string, factory=float
        )


class WordCutter(TextCutter):

    _pattern = re.compile(r"(\S+)")

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        return cut_part_via_regex(self._pattern, arguments_string)


class StringCutter(TextCutter):

    _pattern = re.compile(r"(.+)", flags=re.DOTALL)

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        return cut_part_via_regex(self._pattern, arguments_string)


class ParagraphCutter(TextCutter):
    _pattern = re.compile(r"(.+)")

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        return cut_part_via_regex(self._pattern, arguments_string)


class OptionalCutter(TextCutter):
    def __init__(
        self,
        *,
        default: ty.Optional = None,
        default_factory: ty.Optional[ty.Callable[[], ty.Any]] = None,
        **kwargs
    ) -> None:
        self._default = default
        self._default_factory = default_factory
        TextCutter.__init__(self, **kwargs)

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        try:
            return await self.typevars[0].cut_part(ctx, arguments_string)
        except BadArgumentError:
            if self._default_factory is not None:
                return CutterParsingResponse(
                    parsed_part=self._default_factory(),
                    new_arguments_string=arguments_string,
                )
            else:
                # `None` или установленное значение
                return CutterParsingResponse(
                    parsed_part=self._default,
                    new_arguments_string=arguments_string,
                )


class UnionCutter(TextCutter):
    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        for typevar in self.typevars:
            try:
                parsed_value = await typevar.cut_part(ctx, arguments_string)
            except BadArgumentError:
                continue
            else:
                return parsed_value

        raise BadArgumentError("Regexes didn't matched")


class GroupCutter(TextCutter):
    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        parsed_parts = []
        for typevar in self.typevars:
            try:
                parsed_value = await typevar.cut_part(ctx, arguments_string)
            except BadArgumentError as err:
                raise BadArgumentError("Regexes didn't matched") from err
            else:
                arguments_string = parsed_value.new_arguments_string
                parsed_parts.append(parsed_value.parsed_part)
                continue

        return CutterParsingResponse(
            parsed_part=tuple(parsed_parts),
            new_arguments_string=arguments_string,
        )


class _SequenceCutter(TextCutter):

    _factory: ty.Callable[[list], ty.Sequence]

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        typevar = self.typevars[0]
        parsed_values = []
        while True:
            try:
                parsing_response = await typevar.cut_part(
                    ctx, arguments_string
                )
            except BadArgumentError:
                return CutterParsingResponse(
                    parsed_part=self._factory(parsed_values),
                    new_arguments_string=arguments_string,
                )
            else:
                arguments_string = (
                    parsing_response.new_arguments_string.lstrip()
                    .lstrip(",")
                    .lstrip()
                )
                parsed_values.append(parsing_response.parsed_part)
                continue


class MutableSequenceCutter(_SequenceCutter):

    _factory = list


class ImmutableSequenceCutter(_SequenceCutter):

    _factory = tuple


class UniqueMutableSequenceCutter(_SequenceCutter):

    _factory = set


class UniqueImmutableSequenceCutter(_SequenceCutter):

    _factory = frozenset


class LiteralCutter(TextCutter):
    def __init__(self, container_values: ty.Tuple[str, ...], *args, **kwargs):
        self._container_values = list(map(re.compile, container_values))
        TextCutter.__init__(self, *args, **kwargs)

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        for typevar in self._container_values:
            try:
                return cut_part_via_regex(re.compile(typevar), arguments_string)
            except BadArgumentError:
                continue
        raise BadArgumentError("Regex didn't matched")




UserID = ty.NewType("UserID", int)
GroupID = ty.NewType("GroupID", int)
PageID = ty.NewType("PageID", int)


M = ty.TypeVar("M", UserProvider, GroupProvider, PageProvider, User, Group, Page, UserID, GroupID, PageID)


class Mention(TextCutter, ty.Generic[T]):

    mention_regex = re.compile(
        r"""
        \[
        (?P<page_type>(?:id)|(?:club))  # User or group
        (?P<id>\d+)  # ID of the page
        \|(?P<alias>.+?)  # Alias of the mention
        ]
        """,
        flags=re.X
    )

    def __init__(self, *, typevar: ty.Type[T]):
        self._typevar = typevar
        TextCutter.__init__(self)

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        parsing_response = cut_part_via_regex(self.mention_regex, arguments_string)
        match_object: ty.Match = parsing_response.extra["match_object"]
        parsed_id = int(match_object.group("id"))

        if self._typevar is UserID and match_object.group("page_type") == "id":
            parsing_response.parsed_part = parsed_id
            return parsing_response

        elif self._typevar is GroupID and match_object.group("page_type") == "club":
            parsing_response.parsed_part = parsed_id
            return parsing_response

        elif self._typevar is PageID:
            parsing_response.parsed_part = parsed_id
            return parsing_response

        elif self._typevar is User and match_object.group("page_type") == "id":
            provider = await UserProvider.fetch_one(ctx.api, parsed_id)
            parsing_response.parsed_part = provider.storage
            return parsing_response

        elif self._typevar is Group and match_object.group("page_type") == "club":
            provider = await GroupProvider.fetch_one(ctx.api, parsed_id)
            parsing_response.parsed_part = provider.storage
            return parsing_response

        elif self._typevar is Group and match_object.group("page_type") == "club":
            provider = await GroupProvider.fetch_one(ctx.api, parsed_id)
            parsing_response.parsed_part = provider.storage
            return parsing_response

        else:
            raise BadArgumentError("Mismatched mention kind")


class Entity(TextCutter):
    ...


#
# mention_regex = re.compile(r"\[id(?P<id>\d+)\|(?P<alias>.+?)]")
#
#
# @dataclasses.dataclass
# class UserMention:
#     alias: str
#     user: UserProvider
#
#
# class UserMentionCutter(TextCutter):
#     async def cut_part(
#         self, ctx: Context, arguments_string: str
#     ) -> CutterParsingResponse:
#         parsing_response = cut_part_via_regex(mention_regex, arguments_string)
#         match_object: ty.Match = parsing_response.extra["match_object"]
#         user_object = await UserProvider.fetch_one(ctx.api, int(match_object.group("id")))
#         parsed_part = UserMention(
#             alias=match_object.group("alias"),
#             user=user_object
#         )
#         parsing_response.parsed_part = parsed_part
#         return parsing_response
#
#
# @dataclasses.dataclass
# class RawUserMention:
#     alias: str
#     id: int
#
#
# class RawUserMentionCutter(TextCutter):
#     async def cut_part(
#         self, ctx: Context, arguments_string: str
#     ) -> CutterParsingResponse:
#         parsing_response = cut_part_via_regex(mention_regex, arguments_string)
#         match_object: ty.Match = parsing_response.extra["match_object"]
#         user_id = int(match_object.group("id"))
#         parsed_part = RawUserMention(
#             alias=match_object.group("alias"),
#             id=user_id
#         )
#         parsing_response.parsed_part = parsed_part
#         return parsing_response
#
#
# UserID = ty.NewType("UserID", int)
