class cached_property:
    """
    Дескриптор для создания разово исполняемых property.
    Скопировано с библиотеки `pyramid`.
    """

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.__doc__ = wrapped.__doc__

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val
