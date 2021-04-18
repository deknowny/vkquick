from __future__ import annotations

import abc
import datetime
import typing as ty

import aiohttp

from vkquick.ext.chatbot.utils import get_user_registration_date
from vkquick.ext.chatbot.wrappers.base import Wrapper


class Page(Wrapper, abc.ABC):
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

    @property
    def id(self) -> int:
        return self.fields["id"]

    def mention(self, alias: ty.Optional[str] = None) -> str:
        """
        Создает упоминание пользователя либо с `alias` либо с его именем
        """
        if alias:
            updated_alias = format(self, alias)
            mention = f"[id{self.id}|{updated_alias}]"
        else:
            mention = f"[id{self.id}|{self.fullname}]"
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


class Group(Page):
    @property
    def fullname(self) -> str:
        return self.fields["name"]

    def is_group(self) -> bool:
        return True

    def is_user(self) -> bool:
        return False


class User(Page):
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

    def _extra_fields_to_format(self):
        extra_fields = super()._extra_fields_to_format()
        extra_fields.update(fn=self.fn, ln=self.ln)
        return extra_fields

    async def get_registration_date(
        self, session: ty.Optional[aiohttp.ClientSession] = None
    ) -> datetime.datetime:
        return await get_user_registration_date(self.id, session=session)
