import abc


class Filter(abc.ABC):
    ...

    @abc.abstractmethod
    def decide(self, event: "Event") -> ty.Tuple[bool, str]:
        """
        Возвращает решение: прошел/не прошел, причина
        # TODO
        """
