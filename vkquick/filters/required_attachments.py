import collections
import typing as ty

from vkquick.context import Context
from vkquick.base.filter import Filter, Decision


class RequiredAttachments(Filter):

    passed_decision = Decision(
        True, "Пользователь передал все необходимые вложения"
    )
    not_passed_decision = Decision(
        False, "Пользователь не передал все необходимые вложения"
    )

    def __init__(
        self,
        *,
        photo: ty.Optional[ty.Union[int, range]] = None,
        video: ty.Optional[ty.Union[int, range]] = None,
        audio: ty.Optional[ty.Union[int, range]] = None,
        link: ty.Optional[ty.Union[int, range]] = None,
        wall: ty.Optional[bool] = None,
        wall_reply: ty.Optional[bool] = None,
        sticker: ty.Optional[bool] = None,
        gift: ty.Optional[bool] = None
    ):
        self._required_attachments = {}
        for key, value in locals().items():
            if value is not None and key != "self":
                self._required_attachments[key] = value

    def make_decision(self, context: Context) -> Decision:
        attachments_count = collections.defaultdict(lambda: 0)
        for attachment in context.msg.attachments:
            attachments_count[attachment.type] += 1
        for key, rule in self._required_attachments.items():
            if isinstance(rule, int):
                if attachments_count[key] != rule:
                    return self.not_passed_decision
            else:
                if attachments_count[key] not in rule:
                    return self.not_passed_decision

        return self.passed_decision
