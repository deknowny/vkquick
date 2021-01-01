import abc

from vkquick.json_parsers import json_parser_policy
from vkquick.base.wrapper import Wrapper


class APISerializable(abc.ABC):
    @abc.abstractmethod
    def api_param_representation(self) -> str:
        pass  # pragma: no cover


class UIBuilder(APISerializable):

    scheme = None

    def api_param_representation(self) -> str:
        return json_parser_policy.dumps(self.scheme)


class Attachment(Wrapper, APISerializable):

    _name = None

    def api_param_representation(self) -> str:
        if "access_key" in self.fields:
            access_key = f"_{self.fields.access_key}"
        else:
            access_key = ""

        return (
            f"{self._name}{self.fields.owner_id}_{self.fields.id}{access_key}"
        )
