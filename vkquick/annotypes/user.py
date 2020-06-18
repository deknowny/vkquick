import re
from typing import Optional

import attrdict

from .base import Annotype


class User:
    def __init__(
        self,
        *,
        mention: Optional[str] = None,
        user_id: Optional[int] = None,
        screen_name: Optional[str] = None,
    ):
        if mention is not None:
            if (
                (prep := re.fullmatch(r"\[id(?P<id>\d+)\|.+?\]", mention))
                is not None
            ):
                user_id = prep.group("id")
                user_id = int(user_id)
                self._user_id = user_id
            else:
                raise ValueError(f"{mention} isn't a mention")

        elif user_id is not None:
            self._user_id = user_id

        elif screen_name is not None:
            self._user_id = screen_name

        else:
            raise ValueError("Argmunets haven't been passed")

    async def get_info(self, api, *fields):
        # TODO: Name cases
        print(fields)
        self.info = await api.users.get(
            user_ids=[self._user_id],
            fields=",".join(fields)
        )
        self.info = attrdict.AttrMap(self.info[0])
        # Quick access
        self.fn = self.info.first_name
        self.ln = self.info.last_name
        self.id = self.info.id

        return self

    def mention(self, fstring):
        return f"[id{self.user_id}|{self.__format__(fstring)}]"

    def __str__(self):
        return (
            "<"
            "vq.User "
            f"user_id={self.user_id} "
            f'name="{self.name} {self.lname}"'
            ">"
        )

    def __format__(self, fstring):
        return fstring \
            .replace("<", "{") \
            .replace(">", "}") \
            .format(**self.__dict__)

class UserAnno:
    def __init__(self, *fields):
        self.fields = fields
