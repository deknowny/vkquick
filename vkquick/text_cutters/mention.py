"""
UserMention аргумент
"""
import typing as ty

from vkquick.base.text_cutter import TextCutter, UnmatchedArgument
from vkquick.wrappers.user import User


# TODO: Links parsing (+ init: allows_links)
class UserMention(TextCutter):
    """
    Упоминание пользователя
    """

    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        value, parsed_string = self.cut_part_lite(
            User.mention_regex,
            arguments_string,
            lambda x: int(x.group("id")),
        )
        if value is UnmatchedArgument:
            return value, parsed_string

        return value, parsed_string

    def usage_description(self):
        return "Аргумент является упоминанием пользователя."
