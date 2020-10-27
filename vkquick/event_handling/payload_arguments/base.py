import abc
import typing as ty


class PayloadArgument(abc.ABC):
    """
    Тайпинг к аргументу для реакции у `EventHandler`
    """

    @abc.abstractmethod
    def init_value(
        self, event: "vkquick.events_generators.event.Event"
    ) -> ty.Any:
        """
        Возвращает значение аргумента для реакции. Принимает объект события
        """
