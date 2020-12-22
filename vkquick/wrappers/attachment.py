from __future__ import annotations

from vkquick.base.wrapper import Wrapper
from vkquick.base.serializable import APISerializable


class Attachment(Wrapper, APISerializable):

    _name = None

    def api_param_representation(self) -> str:
        if "access_key" in self.fields:
            access_key = f"_{self.fields.access_key}"
        else:
            access_key = ""

        return f"{self._name}{self.fields.owner_id}_{self.fields.id}{access_key}"


class Photo(Attachment):
    _name = "photo"


class Document(Attachment):
    _name = "doc"



