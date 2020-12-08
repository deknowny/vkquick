"""
ChatOnly фильтр
"""
from vkquick.context import Context
from vkquick.base.filter import Filter, Decision
from vkquick import peer


class ChatOnly(Filter):
    """
    Делает команду доступной только в беседе
    """

    passed_decision = Decision(True, "Сообщение отправлено в чат")
    not_passed_decision = Decision(False, "Сообщение отправлено в лс")

    def make_decision(self, context: Context) -> Decision:
        if context.message.peer_id > peer():
            return self.passed_decision
        return self.not_passed_decision
