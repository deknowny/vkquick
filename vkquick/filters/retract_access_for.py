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
        self._allowed_ids = ids
        self._output = output

        if not ids and output is None:
            raise ValueError("Pass ids or `output` flag in init")

    def make_decision(self, context: Context) -> Decision:
        if context.msg.from_id in self._allowed_ids or (
            self._output is not None and context.msg.out
        ):
            return self.not_passed_decision
        return self.passed_decision
