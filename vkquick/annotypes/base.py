from abc import abstractmethod, ABC


class Annotype(ABC):
    """
    Use for annotation types in your function
    """
    @abstractmethod
    def prepare(self, argname, event, func, bot, bin_stack):
        """
        Called before the argument
        will be inserted to the function
        """
