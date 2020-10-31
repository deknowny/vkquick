import typing as ty

import vkquick.base.filter
import vkquick.events_generators.event


class DirectOnlyDecision(vkquick.base.filter.DecisionEnum):
    DIRECT = vkquick.base.filter.Decision("Сообщение отправлено в личные сообщения")
    not_passed_decision = vkquick.base.filter.Decision("Сообщение не отправлено в личные сообщения")


class DirectOnly(vkquick.base.filter.Filter):

    passed_decision = "Сообщение отправлено в личные сообщения"
    not_passed_decision = "Сообщение не отправлено в личные сообщения"

    def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Tuple[bool, str]:
        """
        Определяет откуда отправлено сообщение
        """
        if event.get_message_object().peer_id < vkquick.peer(0):
            return True, self.passed_decision
        return False, self.not_passed_decision
