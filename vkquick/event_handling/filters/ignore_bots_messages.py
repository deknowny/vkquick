import enum

import vkquick.base.filter
import vkquick.events_generators.event


class IgnoreBotsMessagesStatus(vkquick.base.filter.DecisionStatus):
    PASSED = enum.auto()
    NOT_PASSED = enum.auto()


class IgnoreBotsMessages(vkquick.base.filter.Filter):

    passed_decision = vkquick.base.filter.Decision(True, "Сообщение отправлено от пользователя")
    not_passed_decision = vkquick.base.filter.Decision(False, "Сообщение отправлено от бота")
    passed_response = vkquick.base.filter.FilterResponse(IgnoreBotsMessagesStatus.PASSED, passed_decision)
    not_passed_response = vkquick.base.filter.FilterResponse(IgnoreBotsMessagesStatus.NOT_PASSED, not_passed_decision)

    def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> vkquick.base.filter.FilterResponse:
        """
        Проверяет от кого пришло сообщение
        """
        if event.get_message_object().from_id > 0:
            return self.passed_response
        return self.not_passed_response
