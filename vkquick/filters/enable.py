"""
Enable фильтр
"""
from vkquick.context import Context
from vkquick.base.filter import Filter, Decision


class Enable(Filter):
    """
    Выключатель команды. Используйте,
    если нужно отключить команду, вместо ее
    удаления или убирания из хендлеров бота
    """

    enabled_decision = Decision(
        True, "Обработка команды включена"
    )
    disabled_decision = Decision(
        False, "Обработка команды отключена"
    )

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def make_decision(
        self, context: Context
    ) -> Decision:
        if self.enabled:
            return self.enabled_decision
        return self.disabled_decision
