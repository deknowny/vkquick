import typing

from vkquick.base.api_serializable import APISerializableMixin
from vkquick.json_parsers import json_parser_policy


class UIBuilder(APISerializableMixin):

    scheme: dict
    _dumped_scheme: typing.Optional[str] = None

    def represent_as_api_param(self) -> typing.Union[str, bytes]:
        if self._dumped_scheme is None:
            self._dumped_scheme = json_parser_policy.dumps(self.scheme)
        return self._dumped_scheme
