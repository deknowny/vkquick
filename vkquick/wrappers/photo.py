from __future__ import annotations

from vkquick.base.wrapper import Wrapper


class Photo(Wrapper):
    def __repr__(self):
        if "access_key" in self.fields:
            access_key = f"_{self.fields.access_key}"
        else:
            access_key = ""

        return f"photo{self.fields.owner_id}_{self.fields.id}{access_key}"