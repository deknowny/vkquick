import re
import typing as ty

import vkquick.event_handling.reaction_argument.text_arguments.base
import vkquick.wrappers.user


# TODO: Links parsing (+ init: allows_links)
class UserMention(vkquick.event_handling.reaction_argument.text_arguments.base.TextArgument):

    async def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        value, parsed_string = self.cut_part_lite(
            vkquick.wrappers.user.User.mention_regex, arguments_string, lambda x: int(x.group("id")),
        )
        if value is vkquick.event_handling.reaction_argument.text_arguments.base.UnmatchedArgument:
            return value, parsed_string

        user = await vkquick.wrappers.user.User.build_from_id(value)
        return user, parsed_string

    def usage_description(self, *_):
        return "Аргумент является упоминанием пользователя."
