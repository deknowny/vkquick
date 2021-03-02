from __future__ import annotations
import datetime
import typing as ty

import aiohttp

from vkquick.base.wrapper import Wrapper
from vkquick.utils import (
    get_user_registration_date,
    mark_positional_only,
    cached_property,
)


class PageEntity(Wrapper):
    @property
    def id(self):
        return self.fields.id

    @property
    def fullname(self):
        return (
            self.fields.name
            if "name" in self.fields.name
            else f"{self.fields.first_name} {self.fields.last_name}"
        )

    @property
    def kind(self):
        raise AttributeError(
            "Can't get a kind of entity for this object, "
            "define it by yourself"
        )

class Group(PageEntity):
    @mark_positional_only("alias")
    def mention(self, alias: ty.Optional[str] = None) -> str:
        """
        Создает упоминание пользователя с `alias` либо с его именем
        """
        if alias:
            updated_alias = format(self, alias)
            mention = f"[id{self.id}|{updated_alias}]"
        else:
            mention = f"[id{self.id}|{self.fullname}]"
        return mention

    @property
    def kind(self):
        return "group"


class User(PageEntity):
    @mark_positional_only("alias")
    def mention(self, alias: ty.Optional[str] = None) -> str:
        """
        Создает упоминание пользователя с `alias` либо с его именем
        """
        if alias:
            updated_alias = format(self, alias)
            mention = f"[id{self.id}|{updated_alias}]"
        else:
            mention = f"[id{self.id}|{self.fullname}]"
        return mention

    @property
    def fn(self):
        return self.fields.first_name

    @property
    def ln(self):
        return self.fields.last_name

    @property
    def kind(self):
        return "user"

    def _extra_fields_to_format(self):
        return {"fn": self.fn, "ln": self.ln, "fullname": self.fullname}

    # TODO: cache?
    async def get_registration_date(
        self, session: ty.Optional[aiohttp.ClientSession] = None
    ) -> datetime.datetime:
        return await get_user_registration_date(self.id, session=session)

    def __str__(self):
        return f"<User id={self.id}, fn={self.fn!r}, ln={self.ln!r}>"

    def __format__(self, format_spec):
        format_value = super().__format__(format_spec)
        if format_spec.startswith("@"):
            format_value = format_value[1:]
            format_value = self.mention(format_value)
            return format_value
        return format_value
