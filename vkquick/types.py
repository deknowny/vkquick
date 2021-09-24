import typing

DecoratorFunction = typing.TypeVar(
    "DecoratorFunction", bound=typing.Callable[..., typing.Any]
)
