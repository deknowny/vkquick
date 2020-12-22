from __future__ import annotations

from vkquick.base.wrapper import Wrapper


class Attachment(Wrapper):

    _name = None

    def __repr__(self):
        if "access_key" in self.fields:
            access_key = f"_{self.fields.access_key}"
        else:
            access_key = ""

        return f"{self._name}{self.fields.owner_id}_{self.fields.id}{access_key}"


class Photo(Attachment):
    _name = "photo"


class Document(Attachment):
    _name = "doc"



