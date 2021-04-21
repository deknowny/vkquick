from vkquick.bases.api_serializable import APISerializableMixin
from vkquick.json_parsers import json_parser_policy


class UIBuilder(APISerializableMixin):

    scheme: dict

    def represent_as_api_param(self) -> str:
        return json_parser_policy.dumps(self.scheme)
