from vkquick.bases.event import Event


class GroupEvent(Event):
    @property
    def type(self) -> str:
        return self._content["type"]

    @property
    def object(self) -> dict:
        return self._content["object"]

    @property
    def group_id(self) -> int:
        return self._content["group_id"]


class UserEvent(Event):
    @property
    def type(self) -> int:
        return self._content[0]
