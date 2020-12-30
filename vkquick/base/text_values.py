import typing as ty

import vkquick.base.text_cutter


class TextBase:
    """
    База для текстовых аргументов. Присваивает
    возможность использовать ограничители длины
    """

    def __init__(
        self, max_length: ty.Optional[int] = None, min_length: int = 1
    ) -> None:
        self.check_valid_length(max_length, min_length)
        self.max_length = max_length
        self.min_length = min_length

    @staticmethod
    def check_valid_length(
        max_length: ty.Optional[int], min_length: int
    ) -> None:
        if max_length is not None and max_length < min_length:
            raise ValueError("`max_length` can't be less than `min_length`")
        if max_length is not None and max_length <= 0:
            raise ValueError("`max_length` can't be less or equal 0")
        if min_length <= 0:
            raise ValueError("`min_length` can't be less or equal 0")

    def create_length_rule(self, desc: str) -> str:
        length_rule = "Минимальная длина строки {min_length}, а максимальная {max_length}."
        if self.max_length is None:
            max_length_desc = "не ограничена"
        else:
            max_length_desc = f"меньше или равна {self.max_length}"
        min_length_desc = f"больше или равна {self.min_length}"
        length_rule = length_rule.format(
            min_length=min_length_desc, max_length=max_length_desc
        )
        return desc + length_rule

    def check_range(
        self, got_value: ty.Any, parsed_string: str
    ) -> ty.Tuple[ty.Any, str]:
        if got_value is not vkquick.base.text_cutter.UnmatchedArgument:
            length = len(got_value)
            if length < self.min_length or (
                self.max_length is not None and length > self.max_length
            ):
                return (
                    vkquick.base.text_cutter.UnmatchedArgument,
                    parsed_string,
                )
        return got_value, parsed_string
