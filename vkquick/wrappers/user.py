from __future__ import annotations
import enum
import re
import typing as ty

import pydantic

from vkquick.base.wrapper import Wrapper
import vkquick.utils
import vkquick.utils


mention_regex = re.compile(r"\[id(?P<id>\d+)\|.+?\]")


class User(Wrapper):
    class Config:
        extra = "allow"
        allow_mutation = False
        arbitrary_types_allowed = True

    # TODO: other types
    first_name: str
    last_name: str
    id: int

    @property
    def fn(self):
        return self.first_name

    @property
    def ln(self):
        return self.last_name


class UserField(str, vkquick.utils.AutoLowerNameEnum):
    """
    Параметры для `users.get`
    """

    PHOTO_ID = enum.auto()
    VERIFIED = enum.auto()
    SEX = enum.auto()
    BDATE = enum.auto()
    CITY = enum.auto()
    COUNTRY = enum.auto()
    HOME_TOWN = enum.auto()
    HAS_PHOTO = enum.auto()
    PHOTO_50 = enum.auto()
    PHOTO_100 = enum.auto()
    PHOTO_200_ORIG = enum.auto()
    PHOTO_200 = enum.auto()
    PHOTO_400_ORIG = enum.auto()
    PHOTO_MAX = enum.auto()
    PHOTO_MAX_ORIG = enum.auto()
    ONLINE = enum.auto()
    DOMAIN = enum.auto()
    HAS_MOBILE = enum.auto()
    CONTACTS = enum.auto()
    SITE = enum.auto()
    EDUCATION = enum.auto()
    UNIVERSITIES = enum.auto()
    SCHOOLS = enum.auto()
    STATUS = enum.auto()
    LAST_SEEN = enum.auto()
    FOLLOWERS_COUNT = enum.auto()
    COMMON_COUNT = enum.auto()
    OCCUPATION = enum.auto()
    NICKNAME = enum.auto()
    RELATIVES = enum.auto()
    RELATION = enum.auto()
    PERSONAL = enum.auto()
    CONNECTIONS = enum.auto()
    EXPORTS = enum.auto()
    ACTIVITIES = enum.auto()
    INTERESTS = enum.auto()
    MUSIC = enum.auto()
    MOVIES = enum.auto()
    TV = enum.auto()
    BOOKS = enum.auto()
    GAMES = enum.auto()
    ABOUT = enum.auto()
    QUOTES = enum.auto()
    CAN_POST = enum.auto()
    CAN_SEE_ALL_POSTS = enum.auto()
    CAN_SEE_AUDIO = enum.auto()
    CAN_WRITE_PRIVATE_MESSAGE = enum.auto()
    CAN_SEND_FRIEND_REQUEST = enum.auto()
    IS_FAVORITE = enum.auto()
    IS_HIDDEN_FROM_FEED = enum.auto()
    TIMEZONE = enum.auto()
    SCREEN_NAME = enum.auto()
    MAIDEN_NAME = enum.auto()
    CROP_PHOTO = enum.auto()
    IS_FRIEND = enum.auto()
    FRIEND_STATUS = enum.auto()
    CAREER = enum.auto()
    MILITARY = enum.auto()
    BLACKLISTED = enum.auto()
    BLACKLISTED_BY_ME = enum.auto()
    CAN_BE_INVITED_GROUP = enum.auto()
    FIRST_NAME_NOM = enum.auto()
    FIRST_NAME_GEN = enum.auto()
    FIRST_NAME_DAT = enum.auto()
    FIRST_NAME_ACC = enum.auto()
    FIRST_NAME_INS = enum.auto()
    FIRST_NAME_ABL = enum.auto()
    LAST_NAME_NOM = enum.auto()
    LAST_NAME_GEN = enum.auto()
    LAST_NAME_DAT = enum.auto()
    LAST_NAME_ACC = enum.auto()
    LAST_NAME_INS = enum.auto()
    LAST_NAME_ABL = enum.auto()


class UserNameEnumCase(str, vkquick.utils.AutoLowerNameEnum):
    """
    Падежи к имени в поле `name_case`

    NOM: Именительный
    GEN: Родительный
    DAT: Дательный
    ACC: Винительный
    INS: Творительный
    ABL: Предложный
    """

    NOM = enum.auto()
    GEN = enum.auto()
    DAT = enum.auto()
    ACC = enum.auto()
    INS = enum.auto()
    ABL = enum.auto()
