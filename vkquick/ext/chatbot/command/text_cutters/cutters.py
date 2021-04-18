import abc
import dataclasses
import re
import typing as ty

from vkquick.ext.chatbot.command.context import Context
from vkquick.ext.chatbot.command.text_cutters.base import (
    CutterParsingResponse,
    TextCutter,
    cut_part_via_regex,
)
from vkquick.ext.chatbot.exceptions import BadArgumentError
from vkquick.ext.chatbot.providers.page import (
    GroupProvider,
    PageProvider,
    UserProvider,
)
from vkquick.ext.chatbot.wrappers.page import Group, Page, User


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
        typevar: TextCutter,
        /,
        *,
        default: ty.Optional = None,
        default_factory: ty.Optional[ty.Callable[[], ty.Any]] = None,
        **kwargs,
    ) -> None:
        self._default = default
        self._default_factory = default_factory
        self._typevar = typevar

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        try:
            return await self._typevar.cut_part(ctx, arguments_string)
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
    def __init__(self, *typevars: TextCutter):
        self._typevars = typevars

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        for typevar in self._typevars:
            try:
                parsed_value = await typevar.cut_part(ctx, arguments_string)
            except BadArgumentError:
                continue
            else:
                return parsed_value

        raise BadArgumentError("Regexes didn't matched")


class GroupCutter(TextCutter):
    def __init__(self, *typevars: TextCutter):
        self._typevars = typevars

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        parsed_parts = []
        for typevar in self._typevars:
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

    def __init__(self, typevar: TextCutter):
        self._typevar = typevar

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        typevar = self._typevar
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
    def __init__(self, *container_values: str):
        self._container_values = tuple(map(re.compile, container_values))

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        for typevar in self._container_values:
            try:
                return cut_part_via_regex(typevar, arguments_string)
            except BadArgumentError:
                continue
        raise BadArgumentError("Regex didn't matched")


UserID = ty.NewType("UserID", int)
GroupID = ty.NewType("GroupID", int)
PageID = ty.NewType("PageID", int)

T = ty.TypeVar(
    "T",
    # ty.Type[UserProvider],
    # ty.Type[GroupProvider],
    # ty.Type[PageProvider],
    # ty.Type[User],
    # ty.Type[Group],
    # ty.Type[Page],
    # ty.Type[UserID],
    # ty.Type[GroupID],
    # ty.Type[PageID],
    # covariant=True
)


@dataclasses.dataclass
class Mention(ty.Generic[T]):
    alias: str
    entity: T


class MentionCutter(TextCutter):
    mention_regex = re.compile(
        r"""
        \[
        (?P<page_type>(?:id)|(?:club))  # User or group
        (?P<id>\d+)  # ID of the page
        \|(?P<alias>.+?)  # Alias of the mention
        ]
        """,
        flags=re.X,
    )

    def __init__(self, page_type: T, /):
        self._page_type = page_type

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse[Mention[T]]:
        parsing_response = cut_part_via_regex(
            self.mention_regex, arguments_string
        )
        match_object: ty.Match = parsing_response.extra["match_object"]
        page_id = match_object.group("id")
        page_type = match_object.group("page_type")
        if (
            self._page_type is UserID
            and page_type == "id"
            or self._page_type is GroupID
            and page_type == "club"
            or self._page_type is PageID
        ):
            parsed_part = page_id

        elif (
            self._page_type is UserProvider
            and page_type == "id"
            or self._page_type is GroupProvider
            and page_type == "club"
        ):
            parsed_part = await self._page_type.fetch_one(ctx.api, page_id)

        elif self._page_type is PageProvider:
            if page_type == "id":
                provider_type = UserProvider
            else:
                provider_type = GroupProvider

            parsed_part = await provider_type.fetch_one(ctx.api, page_id)

        elif self._page_type is User and page_type == "id":
            provider = await UserProvider.fetch_one(ctx.api, page_id)
            parsed_part = provider.storage

        elif self._page_type is Group and page_type == "club":
            provider = await GroupProvider.fetch_one(ctx.api, page_id)
            parsed_part = provider.storage

        elif self._page_type is Page:
            if page_type == "id":
                provider_type = UserProvider
            else:
                provider_type = GroupProvider

            provider = await provider_type.fetch_one(ctx.api, page_id)
            parsed_part = provider.storage

        else:
            raise BadArgumentError("Regex didn't matched")

        parsing_response.parsed_part = Mention(
            alias=match_object.group("alias"), entity=parsed_part
        )
        return parsing_response


#
#
# M = ty.TypeVar(
#     "M",
#     UserProvider,
#     GroupProvider,
#     PageProvider,
#     User,
#     Group,
#     Page,
#     ty.Type[UserID],
#     ty.Type[GroupID],
#     ty.Type[PageID],
# )
#
#
# mention_regex_string = r"""
# \[
# (?P<page_type>(?:id)|(?:club))  # User or group
# (?P<id>\d+)  # ID of the page
# \|(?P<alias>.+?)  # Alias of the mention
# ]
# """
#
#
# class _AnyPageCutter(TextCutter, ty.Generic[M]):
#
#     mention_regex = re.compile(mention_regex_string, flags=re.X)
#
#     def __init__(self, *, page_type: ty.Type[T]):
#         self._page_type = page_type
#
#     def __class_getitem__(cls, item: M) -> M:
#         return ty.cast(M, ty.Generic.__class_getitem__(cls, item))
#
#     def make_part(
#         self,
#         ctx: Context,
#         page_id: int,
#         id_owner: ty.Union[ty.Type[UserID], ty.Type[GroupID]],
#     ) -> T:
#         if id_owner is UserID:
#             if self._page_type is UserID:
#                 return page_id
#             elif self._page_type is UserProvider:
#                 return await UserProvider.fetch_one(ctx.api, page_id)
#             elif self._page_type is User:
#                 provider = await UserProvider.fetch_one(ctx.api, page_id)
#                 return provider.storage
#
#         elif id_owner is GroupID:
#             if self._page_type is GroupID:
#                 return page_id
#             elif self._page_type is GroupProvider:
#                 return await GroupProvider.fetch_one(ctx.api, page_id)
#             elif self._page_type is Group:
#                 provider = await GroupProvider.fetch_one(ctx.api, page_id)
#                 return provider.storage
#
#         raise BadArgumentError("Mismatched mention kind")
#
#
# class Mention(_AnyPageCutter[M]):
#
#     def __class_getitem__(cls, item: M) -> int:
#         return ty.cast(M, ty.Generic.__class_getitem__(cls, item))
#
#     async def cut_part(
#         self, ctx: Context, arguments_string: str
#     ) -> CutterParsingResponse:
#
#         parsing_response = cut_part_via_regex(
#             self.mention_regex, arguments_string
#         )
#         match_object: ty.Match = parsing_response.extra["match_object"]
#         parsed_id = int(match_object.group("id"))
#
#         if match_object.group("page_type") == "id":
#             parsing_response.parsed_part = self.make_part(
#                 ctx, parsed_id, UserID
#             )
#         else:
#             parsing_response.parsed_part = self.make_part(
#                 ctx, parsed_id, GroupID
#             )
#
#         return parsing_response
#
#
# class EntityCutter(TextCutter):
#     page_regex = re.compile(
#         rf"""
#         (?:
#
#         |{mention_regex_string})
#         """,
#         flags=re.X,
#     )


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
