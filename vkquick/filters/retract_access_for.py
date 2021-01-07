"""
RetractAccessFor фильтр
"""
import typing as ty

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

    def __init__(self, *ids, output: ty.Optional[bool] = None):
        self.ids = ids
        self.output = output

    def make_decision(self, context: Context) -> Decision:
        if context.msg.from_id not in self.ids or (
            self.output is not None and not context.msg.out
        ):
            return self.passed_decision
        return self.not_passed_decision
