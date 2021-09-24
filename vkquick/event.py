from vkquick.base.event import BaseEvent


class GroupEvent(BaseEvent):
    """
    Обертка над событием в группе
    """

    @property
    def type(self) -> str:
        """
        Тип пришедшего события
        """
        return self._content["type"]

    @property
    def object(self) -> dict:
        """
        Поле `object` пришедшего "update"
        """
        return self._content["object"]

    @property
    def group_id(self) -> int:
        """
        ID группы, в которой случилось событие
        """
        return self._content["group_id"]


class UserEvent(BaseEvent):
    """
    Обертка над событием у пользователя
    """

    @property
    def type(self) -> int:
        """
        Тип пришедшего события
        """
        return self._content[0]

    @property
    def object(self) -> list:
        """
        Сырой объект события (то, что пришло в `updates`)
        """
        return self._content
