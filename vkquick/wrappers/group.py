from __future__ import annotations

import typing as ty

from vkquick.base.wrapper import Wrapper


class Group(Wrapper):
    def mention(self, alias: ty.Optional[str] = None, /) -> str:
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
    def id(self):
        return self.fields.id

    @property
    def fullname(self):
        return self.fields
