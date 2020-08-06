from __future__ import annotations
import re
from typing import Optional

import attrdict

from vkquick import current


class User:
    """
    Позволяет работать с полями пользователя.
    Инициализируется 3мя способами:

    1. `mention`: Строка с упоминанием пользователя. Например, "[id100|Имя Фамилия]"
    1. `user_id`: ID пользователя
    1. `screen_name`: screen_name пользователя. Например: "durov", "deknowny", "id2423423"

    После нужно вызвать крутинный метод `get_info`
    и передать нужные поля, после чего вернется объект пользователя

    В себе содержит:

    * `info`: Все, что было возвращено методом ```users.get```
    * `fn`: Быстрый доступ к имени
    * `ln`: Быстрый доступ к фамилии
    * `id`: Быстрый доступ к ID

    Пользователя можно быстро отформатировать в строку,
    обозначая в <> атрибуты объекта. Например

    `f"{user:<fn> <ln>}"`

    -> `Павел Дуров`

    `f"{user:<fn> (<info.screen_name>)}"`

    -> `Павел (durov)`

    `f"{user:<info.last_name> (<info.screen_name>)}"`

    -> `Дуров (durov)`
    """

    def __init__(
        self,
        *,
        mention: Optional[str] = None,
        user_id: Optional[int] = None,
        screen_name: Optional[str] = None,
    ):
        if mention is not None:
            if (
                prep := re.fullmatch(r"\[id(?P<id>\d+)\|.+?\]", mention)
            ) is not None:
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

    async def get_info(self, *fields, name_case: str = "nom") -> User:
        """
        Получает всю нужную информацию о пользователе методом ```users.get```
        """
        # TODO: Name cases
        self.info = await current.api.users.get(
            user_ids=[self._user_id],
            fields=",".join(fields),
            name_case=name_case,
        )
        self.info = attrdict.AttrMap(self.info[0])
        # Quick access
        self.fn = self.info.first_name
        self.ln = self.info.last_name
        self.id = self.info.id

        return self

    def mention(self, fstring: str) -> str:
        """
        Создает упоминание о пользователе под аллиасом `fstring`
        """
        return f"[id{self.id}|{self.__format__(fstring)}]"

    def __str__(self):
        return (
            "<"
            "vkquick.tools.user.User "
            f"id={self.id} "
            f'name="{self.fn} {self.ln}"'
            ">"
        )

    __repr__ = __str__

    def __format__(self, fstring):
        return (
            fstring.replace("<", "{")
            .replace(">", "}")
            .format(**self.__dict__)
        )


class UserAnno:
    """
    Для создания аннотационных типов,
    работающие с ```users.get```.
    ```__init__``` принимает *fields поле,
    которое передается в ```users.get``` в параметре ```fields```
    """

    def __init__(self, *fields, name_case: str = "nom"):
        self.fields = fields
        self.name_case = name_case
