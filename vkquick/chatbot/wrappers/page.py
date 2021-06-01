from __future__ import annotations

import abc
import datetime
import typing

import aiohttp

from vkquick.chatbot.base.wrapper import Wrapper
from vkquick.chatbot.utils import get_user_registration_date

if typing.TYPE_CHECKING:  # pragma: no cover
    from vkquick.api import API

T = typing.TypeVar("T")
FieldsTypevar = typing.TypeVar("FieldsTypevar")
IDType: typing.TypeAlias = typing.Union[str, int]


class Page(Wrapper, abc.ABC):

    _mention_prefix: str

    @property
    @abc.abstractmethod
    def fullname(self) -> str:
        ...

    @abc.abstractmethod
    def is_group(self) -> bool:
        ...

    @abc.abstractmethod
    def is_user(self) -> bool:
        ...

    @classmethod
    @abc.abstractmethod
    async def fetch_one(
        cls: typing.Type[T],
        api: API,
        id: IDType,
        /,
        *,
        fields: typing.Optional[typing.List[str]] = None,
    ) -> T:
        pass

    @classmethod
    @abc.abstractmethod
    async def fetch_many(
        cls: typing.Type[T],
        api: API,
        /,
        *ids: IDType,
        fields: typing.Optional[typing.List[str]] = None,
    ) -> typing.List[T]:
        pass

    @property
    def id(self) -> int:
        return self.fields["id"]

    def mention(self, alias: typing.Optional[str] = None) -> str:
        """
        Создает упоминание пользователя либо с `alias` либо с его именем
        """
        if alias:
            updated_alias = format(self, alias)
            mention = f"[{self._mention_prefix}{self.id}|{updated_alias}]"
        else:
            mention = f"[{self._mention_prefix}{self.id}|{self.fullname}]"
        return mention

    def _extra_fields_to_format(self) -> dict:
        return {"fullname": self.fullname, "id": self.id}

    def __format__(self, format_spec) -> str:
        format_value = super().__format__(format_spec)
        if format_spec.startswith("@"):
            format_value = format_value[1:]
            format_value = self.mention(format_value)
            return format_value
        return format_value

    def __repr__(self):
        return (
            f"<vkquick.{self.__class__.__name__} fullname={self.fullname!r}>"
        )


class Group(Page):

    _mention_prefix = "club"
    default_fields = ()

    @property
    def fullname(self) -> str:
        return self.fields["name"]

    def is_group(self) -> bool:
        return True

    def is_user(self) -> bool:
        return False

    @classmethod
    async def fetch_one(
        cls: typing.Type[Group],
        api: API,
        id: IDType,
        /,
        *,
        fields: typing.Optional[typing.List[str]] = None,
    ) -> Group:
        group = await api.use_cache().method(
            "groups.get_by_id",
            group_id=id,
            fields=fields or cls.default_fields,
        )
        return cls(group[0])

    @classmethod
    async def fetch_many(
        cls: typing.Type[Group],
        api: API,
        /,
        *ids: IDType,
        fields: typing.Optional[typing.List[str]] = None,
    ) -> typing.List[Group]:
        groups = await api.use_cache().method(
            "groups.get_by_id",
            group_id=ids,
            fields=fields or cls.default_fields,
        )
        groups = [cls(group) for group in groups]
        return groups


class User(Page, typing.Generic[FieldsTypevar]):

    _mention_prefix = "id"
    default_fields = ("sex",)

    def is_group(self) -> bool:
        return False

    def is_user(self) -> bool:
        return True

    @property
    def fullname(self) -> str:
        return f"""{self.fields["first_name"]} {self.fields["last_name"]}"""

    @property
    def id(self):
        return self.fields["id"]

    @property
    def fn(self):
        return self.fields["first_name"]

    @property
    def ln(self):
        return self.fields["last_name"]

    def if_gender(
        self, female: T, male: T = "", default: typing.Optional[T] = None
    ) -> typing.Optional[T]:
        try:
            gender = self.fields["sex"]
        except KeyError as err:
            raise KeyError("Should fetch the user with field `sex`") from err
        else:
            if gender == 1:
                return female
            elif gender == 2:
                return male

            # And gender == 0
            elif default is None:
                return male
            else:
                return default

    def _extra_fields_to_format(self):
        extra_fields = super()._extra_fields_to_format()
        extra_fields.update(fn=self.fn, ln=self.ln)
        return extra_fields

    async def get_registration_date(
        self, session: typing.Optional[aiohttp.ClientSession] = None
    ) -> datetime.datetime:
        return await get_user_registration_date(self.id, session=session)

    @classmethod
    async def fetch_one(
        cls: typing.Type[User],
        api: API,
        id: IDType,
        /,
        *,
        fields: typing.Optional[typing.List[str]] = None,
        name_case: typing.Optional[str] = None,
    ) -> User:
        user = await api.use_cache().method(
            "users.get",
            user_ids=id,
            fields=fields or cls.default_fields,
            name_case=name_case,
        )
        return cls(user[0])

    @classmethod
    async def fetch_many(
        cls: typing.Type[User],
        api: API,
        /,
        *ids: IDType,
        fields: typing.Optional[typing.List[str]] = None,
        name_case: typing.Optional[str] = None,
    ) -> typing.List[User]:
        users = await api.use_cache().method(
            "users.get",
            user_ids=ids,
            fields=fields or cls.default_fields,
            name_case=name_case,
        )
        users = [cls(user) for user in users]
        return users
