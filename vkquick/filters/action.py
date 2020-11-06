"""
Action фильтр
"""
import enum

import vkquick.base.filter
import vkquick.events_generators.event
import vkquick.utils


class ActionStatus(vkquick.base.filter.DecisionStatus):
    """
    Возможные статусы обработки

    * `PASSED`: Событие содержит необходимое действие
    * `ANOTHER_ACTION`: Событие содержит действие, но оно не указано
    * `NOT_PASSED`: Событие не содержит действие
    """

    PASSED = enum.auto()
    ANOTHER_ACTION = enum.auto()
    NOT_PASSED = enum.auto()


class Action(vkquick.base.filter.Filter):
    """
    Фильтр на действие в сообщении (приглашение участников,
    выход из беседы, закрепление сообщения...)
    """

    passed_decision = vkquick.base.filter.Decision(
        True, "В сообщение содержится нужное действие"
    )
    not_passed_decision = vkquick.base.filter.Decision(
        False, "В сообщение не содержится нужное действие"
    )
    another_action_decision = vkquick.base.filter.Decision(
        False, "В сообщение есть действие, но оно не указано для обработки"
    )
    passed_response = vkquick.base.filter.FilterResponse(
        ActionStatus.PASSED, passed_decision
    )
    not_passed_response = vkquick.base.filter.FilterResponse(
        ActionStatus.NOT_PASSED, not_passed_decision
    )
    another_action_response = vkquick.base.filter.FilterResponse(
        ActionStatus.ANOTHER_ACTION, another_action_decision
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

    def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> vkquick.base.filter.FilterResponse:
        message = event.get_message_object()
        if "action" in message:
            if message.action.type in self.handled_actions:
                return self.passed_response
            return self.another_action_response
        return self.not_passed_response
