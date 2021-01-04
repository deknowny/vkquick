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

    def __init__(self, *ids, token_owner: ty.Optional[bool] = None):
        self._allowed_ids = ids
        self._check_token_owner = token_owner

        if not ids and token_owner is None:
            raise ValueError("Pass ids or `token_owner` flag in init")

    def make_decision(self, context: Context) -> Decision:
        if context.msg.from_id in self._allowed_ids or (
            self._check_token_owner is None or context.msg.out
        ):
            return self.passed_decision
        return self.not_passed_decision
