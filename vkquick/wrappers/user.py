from __future__ import annotations
import typing as ty

from vkquick.base.wrapper import Wrapper


class User(Wrapper):
    def mention(self, alias: ty.Optional[str], /) -> str:
        """
        Создает упоминание пользователя с `alias` либо с его именем
        """
        updated_alias = format(self, alias)
        mention = f"[id{self.id}|{updated_alias or self.fn}]"
        return mention

    @property
    def fn(self):
        return self.fields.first_name

    @property
    def ln(self):
        return self.fields.last_name

    @property
    def id(self):
        return self.fields.id

    def extra_fields_to_format(self):
        return {"fn": self.fn, "ln": self.ln}
