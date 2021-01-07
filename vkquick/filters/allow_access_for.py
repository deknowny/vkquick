"""
AllowAccessFor фильтр
"""
import typing as ty

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

    def __init__(self, *ids, output: ty.Optional[bool] = None):
        self._allowed_ids = ids
        self.output = output

        if not ids and output is None:
            raise ValueError("Pass ids or `token_owner` flag in init")

    def make_decision(self, context: Context) -> Decision:
        if context.msg.from_id in self._allowed_ids or (
            self.output is not None and context.msg.out
        ):
            return self.passed_decision
        return self.not_passed_decision
