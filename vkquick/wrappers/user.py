from __future__ import annotations
import enum
import re
import typing as ty

import pydantic

from vkquick.base.wrapper import Wrapper
from vkquick import fetch
from vkquick.utils import AttrDict
import vkquick.utils


mention_regex = re.compile(r"\[id(?P<id>\d+)\|.+?\]")


class User(Wrapper):

    class Config:
        extra = "allow"
        allow_mutation = False
        arbitrary_types_allowed = True

    first_name: str
    id: int
    last_name: str
    can_access_closed: bool
    is_closed: bool
    sex: ty.Optional[int]
    screen_name: ty.Optional[str]
    photo_50: ty.Optional[str]
    photo_100: ty.Optional[str]
    online: ty.Optional[int]
    verified: ty.Optional[int]
    friend_status: ty.Optional[int]
    nickname: ty.Optional[str]
    maiden_name: ty.Optional[str]
    domain: ty.Optional[str]
    bdate: ty.Optional[str]
    city: ty.Optional[AttrDict]
    country: ty.Optional[AttrDict]
    photo_200: ty.Optional[str]
    photo_max: ty.Optional[str]
    photo_200_orig: ty.Optional[str]
    photo_400_orig: ty.Optional[str]
    photo_max_orig: ty.Optional[str]
    photo_id: ty.Optional[str]
    has_photo: ty.Optional[int]
    has_mobile: ty.Optional[int]
    is_friend: ty.Optional[int]
    can_post: ty.Optional[int]
    can_see_all_posts: ty.Optional[int]
    can_see_audio: ty.Optional[int]
    interests: ty.Optional[str]
    books: ty.Optional[str]
    tv: ty.Optional[str]
    quotes: ty.Optional[str]
    about: ty.Optional[str]
    games: ty.Optional[str]
    movies: ty.Optional[str]
    activities: ty.Optional[str]
    music: ty.Optional[str]
    can_write_private_message: ty.Optional[int]
    can_send_friend_request: ty.Optional[int]
    can_be_invited_group: ty.Optional[bool]
    mobile_phone: ty.Optional[str]
    home_phone: ty.Optional[str]
    site: ty.Optional[str]
    status: ty.Optional[str]
    last_seen: ty.Optional[AttrDict]

    @pydantic.validator("city", "country", "last_seen", pre=True)
    def to_attrdict(cls, value):
        return AttrDict(value)

    def mention(self, alias: ty.Optional[str], /) -> str:
        """
        Создает упоминание пользователя с `alias` либо с его именем
        """
        mention = f"[id{self.id}|{alias or self.first_name}]"
        return mention

    @property
    def fn(self):
        return self.first_name

    @property
    def ln(self):
        return self.last_name

    def extra_fields_to_format(self):
        return {
            "fn": self.fn,
            "ln": self.ln
        }


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
