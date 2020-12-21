"""
IgnoreBotsMessages фильтр
"""
from vkquick.context import Context
from vkquick.base.filter import Filter, Decision


class IgnoreBotsMessages(Filter):
    """
    Команда будет игнорировать сообщения от ботов
    """

    passed_decision = Decision(True, "Сообщение отправлено от пользователя")
    not_passed_decision = Decision(False, "Сообщение отправлено от бота")

    def make_decision(self, context: Context) -> Decision:
        if context.msg.from_id > 0:
            return self.passed_decision
        return self.not_passed_decision
