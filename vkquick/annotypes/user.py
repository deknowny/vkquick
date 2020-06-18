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

    async def get_info(self, api):
        self.info = await api.users.get(
            user_ids=[self._user_id],
            fields=[
                "photo_id",
                "verified",
                "sex",
                "bdate",
                "city",
                "country",
                "home_town",
                "has_photo",
                "photo_50",
                "photo_100",
                "photo_200_orig",
                "photo_200",
                "photo_400_orig",
                "photo_max",
                "photo_max_orig",
                "online",
                "domain",
                "has_mobile",
                "contacts",
                "site",
                "education",
                "universities",
                "schools",
                "status",
                "last_seen",
                "followers_count",
                "common_count",
                "occupation",
                "nickname",
                "relatives",
                "relation",
                "personal",
                "connections",
                "exports",
                "activities",
                "interests",
                "music",
                "movies",
                "tv",
                "books",
                "games",
                "about",
                "quotes",
                "can_post",
                "can_see_all_posts",
                "can_see_audio",
                "can_write_private_message",
                "can_send_friend_request",
                "is_favorite",
                "is_hidden_from_feed",
                "timezone",
                "screen_name",
                "maiden_name",
                "crop_photo",
                "is_friend",
                "friend_status",
                "career",
                "military",
                "blacklisted",
                "blacklisted_by_me",
                "can_be_invited_group",
            ],
        )
        self.info = attrdict.AttrMap(self.info[0])
        # Quick access
        self.name = self.info.first_name
        self.lname = self.info.last_name
        self.user_id = self.info.id

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
