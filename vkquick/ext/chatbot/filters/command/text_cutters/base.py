import abc
import typing as ty


from vqchatbot.exceptions import InvalidTextArgumentError


def cut_part_via_regex(
    regex: ty.Pattern,
    arguments_string: str,
) -> str:
    matched = regex.match(arguments_string)
    if matched:
        new_arguments_string = arguments_string[matched.end() :]
        return matched, new_arguments_string

    raise InvalidTextArgumentError


class TextCutter(abc.ABC):
    @abc.abstractmethod
    def cut_part(self, arguments_string: str) -> ty.Tuple[ty.Any, str]:
        ...
