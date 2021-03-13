class EasyDecorator:
    """
    Легкий способ создать класс-декоратор
    """
    def __new__(cls, __handler: ty.Optional[ty.Callable] = None, **kwargs):
        self = object.__new__(cls)
        if __handler is None:
            self.__kwargs = kwargs
            return self.__partail_init
        return self

    def __partail_init(self, __handler: ty.Callable):
        self.__init__(__handler, **self.__kwargs)
        return self