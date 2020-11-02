"""
Enable фильтр
"""
import enum

import vkquick.base.filter
import vkquick.events_generators.event


class EnableStatus(vkquick.base.filter.DecisionStatus):
    ENABLED = enum.auto()
    DISABLED = enum.auto()


class Enable(vkquick.base.filter.Filter):
    """
    Выключатель команды. Используйте,
    если нужно отключить команду, вместо ее
    удаления или убирания из хендлеров бота
    """

    enabled_decision = vkquick.base.filter.Decision(
        True, "Обработка команды включена"
    )
    disabled_decision = vkquick.base.filter.Decision(
        False, "Обработка команды отключена"
    )
    enabled_response = vkquick.base.filter.FilterResponse(
        EnableStatus.ENABLED, enabled_decision
    )
    disabled_response = vkquick.base.filter.FilterResponse(
        EnableStatus.DISABLED, disabled_decision
    )

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> vkquick.base.filter.FilterResponse:
        if self.enabled:
            return self.enabled_response
        return self.disabled_response
