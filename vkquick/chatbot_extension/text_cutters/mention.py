"""
UserMention аргумент
"""
import re
import typing as ty

from vkquick.base.text_cutter import TextCutter


class _Mention(TextCutter):
    def __init__(self, advanced: bool = True):
        self._advanced = advanced


# TODO: Links parsing (+ init: allows_links)
class UserMention(_Mention):
    """
    Упоминание пользователя
    """

    simple_regex = re.compile(r"\[id(?P<id>\d+)\|.+?\]")
    advanced_regex = re.compile(
        r"(?:\[id(\d+)\|.+?\]|(?:id)?(\d+)|(?:https?://)?vk.com/(\d+))"
    )

    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        chunk, remain_string = self.cut_part_lite(
            self.regex,
            arguments_string,
            lambda x: int(x.group("id")),
        )

    def usage_description(self):
        return "Аргумент является упоминанием пользователя."


class GroupMention(_Mention):
    """
    Упоминание пользователя
    """

    regex = re.compile(r"\[club(?P<club>\d+)\|.+?\]")

    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        return self.cut_part_lite(
            self.regex,
            arguments_string,
            lambda x: int(x.group("club")),
        )

    def usage_description(self):
        return "Аргумент является упоминанием группы."
