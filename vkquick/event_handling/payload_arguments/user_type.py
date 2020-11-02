import abc
import typing as ty

import vkquick.base.payload_argument


class UserType(abc.ABC, vkquick.base.payload_argument.PayloadArgument):
    def __init__(
        self,
        *,
        fields: ty.Optional[ty.List[str]] = None,
        name_case: ty.Optional[str] = None
    ) -> None:
        self.fields = fields
        self.name_case = name_case
