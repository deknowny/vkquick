"""
AllowAccessFor фильтр
"""
from vkquick.context import Context
from vkquick.base.filter import Filter, Decision


class AllowAccessFor(Filter):
    """
    Разрешает доступ к команде определенным пользователям/сообществам
    """

    passed_decision = Decision(True, "Пользователь имеет доступ к команде")
    not_passed_decision = Decision(
        False, "Пользователь не имеет доступ к команде"
    )

    def __init__(self, *ids):
        self.ids = ids

    def make_decision(self, context: Context) -> Decision:
        if context.message.from_id in self.ids:
            return self.passed_decision
        return self.not_passed_decision
