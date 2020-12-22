import abc


class APISerializable(abc.ABC):
    @abc.abstractmethod
    def api_param_representation(self) -> str:
        pass
