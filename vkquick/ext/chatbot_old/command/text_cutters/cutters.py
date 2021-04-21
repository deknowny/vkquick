import abc
import dataclasses
import enum
import re
import typing as ty

from vkquick.exceptions import VKAPIError
from vkquick.ext.chatbot.command.context import Context
from vkquick.ext.chatbot.command.text_cutters.base import (
    CutterParsingResponse,
    TextCutter,
    cut_part_via_regex,
)
from vkquick.ext.chatbot.exceptions import BadArgumentError
from vkquick.ext.chatbot.providers.page import (
    GroupProvider,
    IDType,
    PageProvider,
    UserProvider,
)
from vkquick.ext.chatbot.wrappers.page import Group, Page, User


class IntegerCutter(TextCutter):

    _pattern = re.compile(r"[+-]?\d+")

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        return cut_part_via_regex(
            self._pattern, arguments_string, factory=int
        )


class FloatCutter(TextCutter):

    _pattern = re.compile(
        r"""
        [-+]?  # optional sign
        (?:
            (?: \d* \. \d+ )  # .1 .12 .123 etc 9.1 etc 98.1 etc
            |
            (?: \d+ \.? )  # 1. 12. 123. etc 1 12 123 etc
        )
        # followed by optional exponent part if desired
        (?: [Ee][+-]? \d+ )?
        """,
        flags=re.X,
    )

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        return cut_part_via_regex(
            self._pattern, arguments_string, factory=float
        )


class WordCutter(TextCutter):

    _pattern = re.compile(r"\S+")

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        return cut_part_via_regex(self._pattern, arguments_string)


class StringCutter(TextCutter):

    _pattern = re.compile(r".+", flags=re.DOTALL)

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        return cut_part_via_regex(self._pattern, arguments_string)


class ParagraphCutter(TextCutter):
    _pattern = re.compile(r".+")

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


@enum.unique
class PageType(enum.Enum):
    USER = enum.auto()
    GROUP = enum.auto()


@dataclasses.dataclass
class Mention(ty.Generic[T]):
    alias: str
    entity: T


class MentionCutter(TextCutter):
    mention_regex = re.compile(
        r"""
        \[
        (?P<page_type> (?:id) | (?:club) )  # User or group
        (?P<id> [1-9]\d* )  # ID of the page
        \|
        (?P<alias> .+? )  # Alias of the mention
        ]
        """,
        flags=re.X,
    )

    def __init__(
        self,
        page_type: T,
        /,
        user_fields: ty.Optional[ty.List[str]] = None,
        group_fields: ty.Optional[ty.List[str]] = None,
        user_name_case: ty.Optional[str] = None,
    ):
        self._page_type = page_type
        self._user_fields = user_fields
        self._group_fields = group_fields
        self._user_name_case = user_name_case

    async def _make_user_provider(
        self, ctx: Context, page_id: IDType
    ) -> UserProvider:
        return await UserProvider.fetch_one(
            ctx.api,
            page_id,
            fields=self._user_fields,
            name_case=self._user_name_case,
        )

    async def _make_group_provider(
        self, ctx: Context, page_id: IDType
    ) -> GroupProvider:
        return await GroupProvider.fetch_one(
            ctx.api, page_id, fields=self._group_fields
        )

    async def _cast_type(
        self, ctx: Context, page_id: IDType, page_type: PageType
    ) -> T:
        if (
            self._page_type is UserID
            and page_type == PageType.USER
            or self._page_type is GroupID
            and page_type == PageType.GROUP
            or self._page_type is PageID
        ):
            return page_id

        elif self._page_type is UserProvider and page_type == PageType.USER:
            return await self._make_user_provider(ctx, page_id)

        elif self._page_type is GroupProvider and page_type == PageType.GROUP:
            return await self._make_group_provider(ctx, page_id)

        elif self._page_type is PageProvider:
            if page_type == PageType.USER:
                return await self._make_user_provider(ctx, page_id)
            else:
                return await self._make_group_provider(ctx, page_id)

        elif self._page_type is User and page_type == PageType.USER:
            provider = await self._make_user_provider(ctx, page_id)
            return provider.storage

        elif self._page_type is Group and page_type == PageType.GROUP:
            provider = await self._make_group_provider(ctx, page_id)
            return provider.storage

        elif self._page_type is Page:
            if page_type == PageType.USER:
                provider_type = await self._make_user_provider(ctx, page_id)
            else:
                provider_type = await self._make_group_provider(ctx, page_id)

            return provider_type.storage

        else:
            raise BadArgumentError("Regex didn't matched")

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse[Mention[T]]:
        parsing_response = cut_part_via_regex(
            self.mention_regex, arguments_string
        )
        match_object: ty.Match = parsing_response.extra["match_object"]
        page_id = match_object.group("id")
        page_type = match_object.group("page_type")

        if page_type == "id":
            page_type = PageType.USER
        else:
            page_type = PageType.GROUP

        try:
            casted_part = await self._cast_type(ctx, page_id, page_type)
        # Если ID невалидно
        except VKAPIError as err:

            raise BadArgumentError("Invalid id") from err
        else:
            parsing_response.parsed_part = Mention(
                alias=match_object.group("alias"), entity=casted_part
            )
            return parsing_response


class EntityCutter(MentionCutter):

    screen_name_regex = re.compile(
        r"""
        # Optional protocol
        (?: https?:// )? 
        
        # Optional vk domain
        (?: vk\.com/ )?
        
        # Screen name of user or group
        (?P<screen_name> (?: \w+ | \.)+ )
        
        # URL path part
        /?
        
        # Example:
        # vk.com/deknowny
        # vk.com/id100
        # https://vk.com/eee
        """,
        flags=re.X,
    )
    raw_id_regex = re.compile(
        r"""
        # Type of id: group/user. Positive ID means user, negative -- group
        (?P<type>
            [+-]? | (?:id) | (?:club)
        ) 
        
        # ID of user/group
        (?P<id> \d+ ∂)
        """,
        flags=re.X,
    )

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        for method in (
            self._mention_method(ctx, arguments_string),
            self._link_method(ctx, arguments_string),
            self._raw_id_method(ctx, arguments_string),
            self._attached_method(ctx, arguments_string),
        ):
            try:
                return await method
            except BadArgumentError:
                continue

        raise BadArgumentError("Regexes didn't matched, no user attached")

    async def _mention_method(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        parsing_response = await MentionCutter.cut_part(
            self, ctx, arguments_string
        )
        parsing_response.parsed_part = parsing_response.parsed_part.entity
        return parsing_response

    async def _link_method(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        parsing_response = cut_part_via_regex(
            self.screen_name_regex, arguments_string, group="screen_name"
        )
        resolved_screen_name = await ctx.api.utils.resolve_screen_name(
            screen_name=parsing_response.parsed_part
        )
        if not resolved_screen_name:
            raise BadArgumentError("Invalid screen name")

        if resolved_screen_name["type"] == "user":
            page_type = PageType.USER
        elif resolved_screen_name["type"] == "user":
            page_type = PageType.GROUP
        else:
            raise BadArgumentError("Invalid screen name")

        parsing_response.parsed_part = await self._cast_type(
            ctx, resolved_screen_name["object_id"], page_type
        )

        return parsing_response

    async def _raw_id_method(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        parsing_response = cut_part_via_regex(
            self.raw_id_regex, arguments_string
        )
        match_object: ty.Match = parsing_response.extra["match_object"]

        if match_object.group("type") in ("+", "id", ""):
            page_type = PageType.USER
        else:
            page_type = PageType.GROUP

        parsing_response.parsed_part = await self._cast_type(
            ctx, match_object.group("id"), page_type
        )

        return parsing_response

    async def _attached_method(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        if ctx.msg.reply_message is not None:
            page_id = ctx.msg.reply_message.from_id
            if ctx.extra.get("replied_user_used") is None:
                ctx.extra["replied_user_used"] = ...
            else:
                raise BadArgumentError("No user attached")
        else:
            forwarded_pages = ctx.msg.fwd_messages
            step = ctx.extra.get("forward_page_iter_step")
            if step is None:
                ctx.extra["forward_page_iter_step"] = 1
                step = 0
            else:
                ctx.extra["forward_page_iter_step"] += 1
            try:
                page_id = forwarded_pages[step].from_id
            except IndexError:
                raise BadArgumentError("No user attached")

        parsed_part = await self._cast_type(
            ctx,
            abs(page_id),
            PageType.USER if page_id > 0 else PageType.GROUP,
        )

        return CutterParsingResponse(
            parsed_part=parsed_part, new_arguments_string=arguments_string
        )
