import dataclasses
import enum
import re
import typing

from vkquick.chatbot.base.cutter import (
    Cutter,
    CutterParsingResponse,
    cut_part_via_regex,
    html_list_to_message,
)
from vkquick.chatbot.exceptions import BadArgumentError
from vkquick.chatbot.storages import NewMessage
from vkquick.chatbot.utils import get_origin_typing
from vkquick.chatbot.wrappers.page import Group, Page, User
from vkquick.exceptions import APIError


class IntegerCutter(Cutter):
    _pattern = re.compile(r"[+-]?\d+")

    async def cut_part(
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse[int]:
        return cut_part_via_regex(
            self._pattern,
            arguments_string,
            factory=int,
            error_description=self.gen_message_doc(),
        )

    def gen_doc(self):
        return "целое положительное или отрицательное число"


class FloatCutter(Cutter):
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
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse[float]:
        return cut_part_via_regex(
            self._pattern,
            arguments_string,
            factory=float,
            error_description=self.gen_message_doc(),
        )

    def gen_doc(self):
        return (
            "дробное положительное или отрицательное число "
            "в десятичной форме (3.14, 2.718...). "
            "Число также может быть записано в "
            "экспоненциальной форме (4e6, 3.5E-6...). "
            "Если целая часть равна нулю, то она может быть опущена: "
            ".45 это 0.45 "
        )


class WordCutter(Cutter):
    _pattern = re.compile(r"\S+")

    async def cut_part(
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse[str]:
        return cut_part_via_regex(
            self._pattern,
            arguments_string,
            error_description=self.gen_message_doc(),
        )

    def gen_doc(self):
        return "любое слово (последовательность непробельных символов)"


class StringCutter(Cutter):
    _pattern = re.compile(r".+", flags=re.DOTALL)

    async def cut_part(
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse[str]:
        return cut_part_via_regex(
            self._pattern,
            arguments_string,
            error_description=self.gen_message_doc(),
        )

    def gen_doc(self):
        return "абсолютно любой текст"


class OptionalCutter(Cutter):
    def __init__(
        self,
        typevar: Cutter,
        /,
        *,
        default: typing.Optional = None,
        default_factory: typing.Optional[
            typing.Callable[[], typing.Any]
        ] = None,
    ) -> None:
        self._default = default
        self._default_factory = default_factory
        self._typevar = typevar

    async def cut_part(
        self, ctx: NewMessage, arguments_string: str
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

    def gen_doc(self):
        typevar_docstring = self._typevar.gen_doc()
        default = (
            f"(по умолчанию — {self._default!r})"
            if self._default is not None
            else ""
        )
        return (
            typevar_docstring
            + f"\nАргумент опционален и может быть опущен {default}"
        )


class UnionCutter(Cutter):

    def __init__(self, *typevars: Cutter):
        self._typevars = typevars

    async def cut_part(
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse:
        for typevar in self._typevars:
            try:
                parsed_value = await typevar.cut_part(ctx, arguments_string)
            except BadArgumentError:
                continue
            else:
                return parsed_value

        raise BadArgumentError(self.gen_message_doc())

    def gen_doc(self):
        header = "одно из следующих значений:<br><ol>{elements}</ol>"
        elements_docs = [
            f"<li>{typevar.gen_doc().capitalize()}</li>"
            for typevar in self._typevars
        ]
        elements_docs = "\n".join(elements_docs)
        return header.format(elements=elements_docs)


class GroupCutter(Cutter):
    def __init__(self, *typevars: Cutter):
        self._typevars = typevars

    async def cut_part(
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse:
        parsed_parts = []
        for typevar in self._typevars:
            try:
                parsed_value = await typevar.cut_part(ctx, arguments_string)
            except BadArgumentError as err:
                raise BadArgumentError(self.gen_message_doc()) from err
            else:
                arguments_string = parsed_value.new_arguments_string
                parsed_parts.append(parsed_value.parsed_part)
                continue

        return CutterParsingResponse(
            parsed_part=tuple(parsed_parts),
            new_arguments_string=arguments_string,
        )

    def gen_doc(self):
        header = "последовательность следующих аргументов без пробелов:<br><ol>{elements}</ol>"
        elements_docs = [
            f"<li>{typevar.gen_doc()}</li>" for typevar in self._typevars
        ]
        elements_docs = "\n".join(elements_docs)
        return header.format(elements=elements_docs)


class _SequenceCutter(Cutter):
    _factory: typing.Callable[[list], typing.Sequence]

    def __init__(self, typevar: Cutter):
        self._typevar = typevar

    async def cut_part(
        self, ctx: NewMessage, arguments_string: str
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

    def gen_doc(self):
        typevar_docstring = self._typevar.gen_doc()
        return (
            typevar_docstring
            + f". Аргументов может быть несколько (перечислены через запятую/пробел)"
        )


class MutableSequenceCutter(_SequenceCutter):
    _factory = list


class ImmutableSequenceCutter(_SequenceCutter):
    _factory = tuple


class UniqueMutableSequenceCutter(_SequenceCutter):
    _factory = set


class UniqueImmutableSequenceCutter(_SequenceCutter):
    _factory = frozenset


class LiteralCutter(Cutter):

    def __init__(self, *container_values: str):
        self._container_values = tuple(map(re.compile, container_values))

    async def cut_part(
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse:
        for typevar in self._container_values:
            try:
                return cut_part_via_regex(typevar, arguments_string)
            except BadArgumentError:
                continue
        raise BadArgumentError(self.gen_message_doc())

    def gen_doc(self):
        header = "любое из следующих значений:<br><ol>{elements}</ol>"
        elements_docs = [
            f"<li><code>{typevar.pattern}</code></li>"
            for typevar in self._container_values
        ]
        elements_docs = "\n".join(elements_docs)
        return header.format(elements=elements_docs)


UserID = typing.NewType("UserID", int)
GroupID = typing.NewType("GroupID", int)
PageID = typing.NewType("PageID", int)

T = typing.TypeVar(
    "T",
    # typing.Type[UserProvider],
    # typing.Type[GroupProvider],
    # typing.Type[PageProvider],
    # typing.Type[User],
    # typing.Type[Group],
    # typing.Type[Page],
    # typing.Type[UserID],
    # typing.Type[GroupID],
    # typing.Type[PageID],
    # covariant=True
)


@enum.unique
class PageType(enum.Enum):
    USER = enum.auto()
    GROUP = enum.auto()


@dataclasses.dataclass
class Mention(typing.Generic[T]):
    alias: str
    entity: T
    page_type: PageType


class MentionCutter(Cutter):
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
    ):
        self._page_type = get_origin_typing(page_type)
        fields = typing.get_args(page_type)
        if fields:
            self._fields = typing.get_args(fields[0])
        else:
            self._fields = None

    async def _make_user(self, ctx: NewMessage, page_id: int):
        return await User.fetch_one(ctx.api, page_id, fields=self._fields)

    async def _make_group(self, ctx: NewMessage, page_id: int):
        return await Group.fetch_one(ctx.api, page_id, fields=self._fields)

    async def _cast_type(
        self, ctx: NewMessage, page_id: int, page_type: PageType
    ) -> T:
        if (
            self._page_type is UserID
            and page_type == PageType.USER
            or self._page_type is GroupID
            and page_type == PageType.GROUP
            or self._page_type is PageID
        ):
            return page_id

        elif self._page_type is User and page_type == PageType.USER:
            return await self._make_user(ctx, page_id)

        elif self._page_type is Group and page_type == PageType.GROUP:
            return await self._make_group(ctx, page_id)

        elif self._page_type is Page:
            if page_type == PageType.USER:
                return await self._make_user(ctx, page_id)
            else:
                return await self._make_group(ctx, page_id)

        else:
            raise BadArgumentError(self.gen_doc())

    async def cut_part(
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse[Mention[T]]:
        parsing_response = cut_part_via_regex(
            self.mention_regex, arguments_string
        )
        match_object: typing.Match = parsing_response.extra["match_object"]
        page_id = int(match_object.group("id"))
        page_type = match_object.group("page_type")

        if page_type == "id":
            page_type = PageType.USER
        else:
            page_type = PageType.GROUP

        try:
            casted_part = await self._cast_type(ctx, page_id, page_type)
        # Если ID невалидно
        except APIError as err:
            raise BadArgumentError("Invalid id") from err
        else:
            parsing_response.parsed_part = Mention(
                alias=match_object.group("alias"),
                entity=casted_part,
                page_type=page_type,
            )
            return parsing_response

    def gen_doc(self):
        if self._page_type in {User, UserID}:
            who = "пользователь"
        elif self._page_type in {Group, GroupID}:
            who = "группа"
        else:
            who = "пользователь или группа"
        return f"{who} в виде упоминания"


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
        (?P<id> \d+ )
        """,
        flags=re.X,
    )

    def gen_doc(self):
        if self._page_type in {User, UserID}:
            who = "пользователя"
        elif self._page_type in {Group, GroupID}:
            who = "группы"
        else:
            who = "пользователя или группы"
        return (
            f"упоминание/ID/короткое имя/ссылку на страницу {who}. "
            "Также можно просто переслать сообщение пользователя"
        )

    async def cut_part(
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse:
        for method in (
            self._mention_method,
            self._link_method,
            self._raw_id_method,
            self._attached_method,
        ):
            try:
                return await method(ctx, arguments_string)
            except BadArgumentError:
                continue

        raise BadArgumentError(self.gen_doc())

    async def _mention_method(
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse:
        parsing_response = await MentionCutter.cut_part(
            self, ctx, arguments_string
        )
        parsing_response.parsed_part = parsing_response.parsed_part.entity
        return parsing_response

    async def _link_method(
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse:
        parsing_response = cut_part_via_regex(
            self.screen_name_regex, arguments_string, group="screen_name"
        )

        resolved_screen_name = await ctx.api.use_cache().method(
            "utils.resolve_screen_name",
            screen_name=parsing_response.parsed_part,
        )
        if not resolved_screen_name:
            raise BadArgumentError("Invalid screen name")

        if resolved_screen_name["type"] == "user":
            page_type = PageType.USER
        elif resolved_screen_name["type"] == "group":
            page_type = PageType.GROUP
        else:
            raise BadArgumentError("Invalid screen name")

        parsing_response.parsed_part = await self._cast_type(
            ctx, resolved_screen_name["object_id"], page_type
        )

        return parsing_response

    async def _raw_id_method(
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse:
        parsing_response = cut_part_via_regex(
            self.raw_id_regex, arguments_string
        )
        match_object: typing.Match = parsing_response.extra["match_object"]

        if match_object.group("type") in ("+", "id", ""):
            page_type = PageType.USER
        else:
            page_type = PageType.GROUP

        parsing_response.parsed_part = await self._cast_type(
            ctx, match_object.group("id"), page_type
        )

        return parsing_response

    async def _attached_method(
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse:
        if ctx.msg.is_cropped:
            await ctx.msg.extend(ctx.api)
        if ctx.msg.reply_message is not None:
            page_id = ctx.msg.reply_message.from_id
            if (
                ctx.argument_processing_payload.get("_replied_user_used")
                is None
            ):
                ctx.argument_processing_payload["_replied_user_used"] = ...
            else:
                raise BadArgumentError("No user attached")
        else:
            forwarded_pages = ctx.msg.fwd_messages
            step = ctx.argument_processing_payload.get(
                "_forward_page_iter_step"
            )
            if step is None:
                ctx.argument_processing_payload["_forward_page_iter_step"] = 1
                step = 0
            else:
                ctx.argument_processing_payload[
                    "_forward_page_iter_step"
                ] += 1
            try:
                page_id = forwarded_pages[step].from_id
            except IndexError:
                raise BadArgumentError(self.gen_doc())

        parsed_part = await self._cast_type(
            ctx,
            abs(page_id),
            PageType.USER if page_id > 0 else PageType.GROUP,
        )

        return CutterParsingResponse(
            parsed_part=parsed_part, new_arguments_string=arguments_string
        )


class BoolCutter(Cutter):
    true_values = ["1", "да", "+", "on", "вкл"]
    false_values = ["0", "no", "-", "off", "выкл"]

    async def cut_part(
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse[bool]:
        for true_value in self.true_values:
            if arguments_string.startswith(true_value):
                new_arguments_string = arguments_string[len(true_value) :]
                return CutterParsingResponse(
                    parsed_part=True,
                    new_arguments_string=new_arguments_string,
                )
        for false_value in self.false_values:
            if arguments_string.startswith(false_value):
                new_arguments_string = arguments_string[len(false_value) :]
                return CutterParsingResponse(
                    parsed_part=False,
                    new_arguments_string=new_arguments_string,
                )

        raise BadArgumentError(self.gen_doc())

    def gen_doc(self) -> str:
        return "булево значение: {} в качестве истины и {} для лжи".format(
            "/".join(self.true_values),
            "/".join(self.false_values),
        )
