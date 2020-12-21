"""
RetractAccessFor фильтр
"""
from vkquick.context import Context
from vkquick.base.filter import Filter, Decision


class RetractAccessFor(Filter):
    """
    Ограничивает пользование командой определенным людям/сообществам
    """

    passed_decision = Decision(
        True, "Пользователь может пользоваться командой"
    )
    not_passed_decision = Decision(
        False, "Пользователь не может пользоваться командой"
    )

    def __init__(self, *ids):
        self.ids = ids

    def make_decision(self, context: Context) -> Decision:
        if context.msg.from_id not in self.ids:
            return self.passed_decision
        return self.not_passed_decision
