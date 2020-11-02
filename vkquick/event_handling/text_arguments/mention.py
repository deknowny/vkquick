"""
UserMention аргумент
"""
import typing as ty

import vkquick.base.text_argument
import vkquick.wrappers.user


# TODO: Links parsing (+ init: allows_links)
class UserMention(vkquick.base.text_argument.TextArgument):
    """
    Упоминание пользователя
    """

    async def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        value, parsed_string = self.cut_part_lite(
            vkquick.wrappers.user.User.mention_regex,
            arguments_string,
            lambda x: int(x.group("id")),
        )
        if value is vkquick.base.text_argument.UnmatchedArgument:
            return value, parsed_string

        user = await vkquick.wrappers.user.User.build_from_id(value)
        return user, parsed_string

    def usage_description(self):
        return "Аргумент является упоминанием пользователя."
