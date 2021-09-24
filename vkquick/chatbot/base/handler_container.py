import dataclasses
import typing

HandlerTypevar = typing.TypeVar(
    "HandlerTypevar", bound=typing.Callable[..., typing.Awaitable]
)


@dataclasses.dataclass
class HandlerMixin(typing.Generic[HandlerTypevar]):
    handler: HandlerTypevar
