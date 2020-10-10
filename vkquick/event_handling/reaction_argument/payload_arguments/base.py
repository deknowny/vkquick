import abc
import typing as ty

import vkquick.event_handling.reaction_argument.base
import vkquick.events_generators.event


class PayloadArgument(
    vkquick.event_handling.reaction_argument.base.ReactionArgument, abc.ABC
):
    """
    Тайпинг к аргументу для реакции у `EventHandler`
    """

    @abc.abstractmethod
    def init_value(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Any:
        """
        Возвращает значение аргумента для рекакции. Принимает объект события
        """
