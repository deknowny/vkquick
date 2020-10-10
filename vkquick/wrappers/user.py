from __future__ import annotations
import re
import typing as ty

import attrdict

import vkquick.wrappers.base
import vkquick.current
import vkquick.utils


class User(vkquick.wrappers.base.Wrapper):

    api = vkquick.current.fetch("user_wrapper_api", "api")
    mention_regex = re.compile(r"\[id(\d+)\|.+?\]")

    def __init__(self, scheme: attrdict.AttrMap):
        super().__init__(scheme)
        self.add_field_shortcut("fn", scheme.first_name)
        self.add_field_shortcut("ln", scheme.last_name)
        self.add_field_shortcut("id", scheme.id)

    @classmethod
    async def build_from_id(cls, id_: ty.Union[int, str], /) -> User:
        """
        Создает обертку над юзером через его ID или screen name
        """
        users = await cls.api.__get__(cls).users.get(user_ids=id_)
        self = cls(users[0])
        return self

    @classmethod
    async def build_from_mention(cls, mention: str, /) -> User:
        """
        Создает обертку над юзером через упоминание пользователя
        """
        match = cls.mention_regex.fullmatch(mention)
        if not match:
            raise ValueError(f"`{mention}` isn't a user mention")

        user_id = match.group(1)
        return await cls.build_from_id(user_id)

    def mention(self, alias: str, /) -> str:
        new_alias = self.__format__(alias)
        mention = f"[id{self.scheme.id}|{new_alias}]"
        return mention

    def __format__(self, format_spec: str) -> str:
        inserted_values = vkquick.utils.SafeDict(
            scheme=self.scheme,
            **self.shortcuts
        )
        return format_spec.format_map(inserted_values)

