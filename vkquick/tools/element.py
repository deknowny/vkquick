from typing import Optional, List

from .ui import UI
from .button import Button


class Element(UI):
    """
    Элемент карусели
    """

    def __init__(
        self,
        *,
        buttons: List[Button],
        title: Optional[str] = None,
        description: Optional[str] = None,
        photo_id: Optional[int] = None
    ):
        self.info = dict(buttons=[but.info for but in buttons], action={})
        if title is not None:
            self.info.update(title=title)
        if description is not None:
            self.info.update(description=description)
        if photo_id is not None:
            self.info.update(photo_id=photo_id)

    def open_link(self, link):
        self.info["action"] = dict(type="open_link", link=link)
        return self

    def open_photo(self):
        self.info["action"] = dict(type="open_photo")
        return self
