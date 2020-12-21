"""
Action фильтр
"""
from vkquick.context import Context
from vkquick.base.filter import Filter, Decision


class Action(Filter):
    """
    Фильтр на действие в сообщении (приглашение участников,
    выход из беседы, закрепление сообщения...)
    """

    passed_decision = Decision(True, "В сообщение содержится нужное действие")
    not_passed_decision = Decision(
        False, "В сообщение не содержится нужное действие"
    )
    another_action_decision = Decision(
        False, "В сообщение есть действие, но оно не указано для обработки"
    )

    def __init__(
        self,
        *extra_actions,
        chat_photo_update: bool = False,
        chat_photo_remove: bool = False,
        chat_create: bool = False,
        chat_title_update: bool = False,
        chat_invite_user: bool = False,
        chat_kick_user: bool = False,
        chat_pin_message: bool = False,
        chat_unpin_message: bool = False,
        chat_invite_user_by_link: bool = False,
        chat_screenshot: bool = False
    ) -> None:
        types = locals().copy()
        types.pop("self")
        extra = types.pop("extra_actions")
        self.handled_actions = [key for key, value in types.items() if value]
        self.handled_actions.extend(extra)
        self._check_actions_count()

    def _check_actions_count(self):
        """
        Проверяет, чтобы хотя какое-то из событий
        было передано в момент инициализации
        """
        if not self.handled_actions:
            raise ValueError(
                "Action filters should have at "
                "least 1 type, got nothing in __init__"
            )

    def make_decision(self, context: Context) -> Decision:
        if "action" in context.msg:
            if context.msg.action.type in self.handled_actions:
                return self.passed_decision
            return self.another_action_decision
        return self.not_passed_decision
