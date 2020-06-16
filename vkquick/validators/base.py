from abc import abstractmethod, ABC


class Validator(ABC):
    def __call__(self, func):
        if hasattr(func, "validators"):
            func.validators.append(self)

    @abstractmethod
    def isvalid(self, event, com, bot, bin_stack):
        """
        Is def valid or not
        """
