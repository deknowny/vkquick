import typing as ty

import vkquick.base.filter
import vkquick.events_generators.event


class ChatOnly(vkquick.base.filter.Filter):

    passed_decision = "Сообщение отправлено с чата"
    not_passed_decision = "Сообщение не отправлено с чата"

    def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Tuple[bool, str]:
        if event.get_message_object().peer_id > vkquick.peer(0):
            return True, self.passed_decision
        return False, self.not_passed_decision
