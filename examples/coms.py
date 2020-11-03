from __future__ import annotations
import typing as ty

import vkquick as vq


# @vq.Command(
#     prefixes=["/", "!"],
#     names=["foo", "bar"],
# )
# async def foo(ctx, name: str, *, desc: str):
#     ...
#
#
# def bar():
#     ...
#
# @vq.Command(
#     prefixes=["!"],
#     names=["desc"]
# )
# def spam(*, desc: str):
#     ...

# def __init__(
#     self, *,
#     title: str,
#     description: str,
#     type_transformer: ty.Callable[[str], ty.Tuple[str, ty.Any]],
# ):
#     locals()

T = ty.TypeVar("T")

class DefaultFactory: ...


class Argument(ty.Generic[T]):

    def __init__(
        self, *,
        title: ty.Optional[str] = None,
        description: ty.Optional[str] = None,
        type_transformer: ty.Callable[[str], ty.Tuple[str, ty.Any]] = None,
    ):
        locals()

    def __class_getitem__(cls, item: T) -> ty.Type[Argument]:
        return super().__class_getitem__(item)

    def __call__(self) -> T:
        ...


@vq.Enable
@vq.Command(names=["foo"])
def foo(
    arg1: Argument[str](),
    arg2: Argument[vq.String],
):
    return arg1, arg2


@foo.on_invalid_filter(vq.Enable)
def foo_invalid_enable(ctx):
    ...


@foo.on_invalid_argument("arg1")
def foo_invalid_arg1(ctx, value):
    ...












print(foo1("1 2 3"))