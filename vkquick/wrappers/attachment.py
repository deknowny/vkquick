from __future__ import annotations

from vkquick.base.serializable import Attachment


class Photo(Attachment):
    _name = "photo"


class Document(Attachment):
    _name = "doc"
