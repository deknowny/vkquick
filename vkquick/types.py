import typing as ty


DecoratorFunction = ty.TypeVar(
    "DecoratorFunction", bound=ty.Callable[..., ty.Any]
)
