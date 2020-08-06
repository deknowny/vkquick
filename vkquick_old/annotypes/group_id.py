from .base import Annotype


class GroupID(Annotype):
    """
    Возаращет ID группы, где произошло событие
    """

    def prepare(self, argname, event, func, bin_stack) -> int:
        return event.group_id
