from __future__ import annotations

import inspect
import typing

from vkquick.chatbot.base.cutter import Argument, CommandTextArgument, Cutter
from vkquick.chatbot.command.cutters import (
    BoolCutter,
    EntityCutter,
    FloatCutter,
    GroupCutter,
    GroupID,
    ImmutableSequenceCutter,
    IntegerCutter,
    LiteralCutter,
    Mention,
    MentionCutter,
    MutableSequenceCutter,
    OptionalCutter,
    PageID,
    StringCutter,
    UnionCutter,
    UniqueImmutableSequenceCutter,
    UniqueMutableSequenceCutter,
    UserID,
    WordCutter,
)
from vkquick.chatbot.wrappers.page import Group, Page, User


def resolve_typing(parameter: inspect.Parameter) -> CommandTextArgument:
    if isinstance(parameter.default, Argument):
        arg_settings = parameter.default
    elif parameter.default != parameter.empty:
        arg_settings = Argument(default=parameter.default)
    else:
        arg_settings = Argument()

    if (
        arg_settings.default is not None
        or arg_settings.default_factory is not None
        and not typing.get_origin(parameter.annotation) is typing.Union
    ):
        arg_annotation = typing.Optional[parameter.annotation]
    else:
        arg_annotation = parameter.annotation

    cutter = _resolve_cutter(
        arg_name=parameter.name,
        arg_annotation=arg_annotation,
        arg_settings=arg_settings,
        arg_kind=parameter.kind,
    )
    return CommandTextArgument(
        argument_name=parameter.name,
        argument_settings=arg_settings,
        cutter=cutter,
    )


def _resolve_cutter(
    *,
    arg_name: str,
    arg_annotation: typing.Any,
    arg_settings: Argument,
    arg_kind,
) -> Cutter:
    if arg_annotation is int:
        return IntegerCutter()
    elif arg_annotation is float:
        return FloatCutter()
    elif arg_annotation is bool:
        return BoolCutter()
    elif arg_annotation is str:
        if arg_kind == inspect.Parameter.KEYWORD_ONLY:
            return StringCutter()
        else:
            return WordCutter()

    # Optional
    elif typing.get_origin(arg_annotation) is typing.Union and type(
        None
    ) in typing.get_args(arg_annotation):
        return OptionalCutter(
            _resolve_cutter(
                arg_name=arg_name,
                arg_annotation=typing.get_args(arg_annotation)[0],
                arg_settings=arg_settings,
                arg_kind=arg_kind,
            ),
            default=arg_settings.default,
            default_factory=arg_settings.default_factory,
        )
    # Union
    elif typing.get_origin(arg_annotation) is typing.Union:
        typevar_cutters = (
            _resolve_cutter(
                arg_name=arg_name,
                arg_annotation=typevar,
                arg_settings=arg_settings,
                arg_kind=arg_kind,
            )
            for typevar in typing.get_args(arg_annotation)
        )
        return UnionCutter(*typevar_cutters)

    # List
    elif typing.get_origin(arg_annotation) is list:
        typevar_cutter = _resolve_cutter(
            arg_name=arg_name,
            arg_annotation=typing.get_args(arg_annotation)[0],
            arg_settings=arg_settings,
            arg_kind=arg_kind,
        )
        return MutableSequenceCutter(typevar_cutter)
    # Tuple sequence
    elif typing.get_origin(
        arg_annotation
    ) is tuple and Ellipsis in typing.get_args(arg_annotation):
        typevar_cutter = _resolve_cutter(
            arg_name=arg_name,
            arg_annotation=typing.get_args(arg_annotation)[0],
            arg_settings=arg_settings,
            arg_kind=arg_kind,
        )
        return ImmutableSequenceCutter(typevar_cutter)

    # Tuple
    elif typing.get_origin(
        arg_annotation
    ) is tuple and Ellipsis not in typing.get_args(arg_annotation):

        typevar_cutters = (
            _resolve_cutter(
                arg_name=arg_name,
                arg_annotation=typevar,
                arg_settings=arg_settings,
                arg_kind=arg_kind,
            )
            for typevar in typing.get_args(arg_annotation)
        )

        return GroupCutter(*typevar_cutters)

    # Set
    elif typing.get_origin(arg_annotation) is set:
        typevar_cutter = _resolve_cutter(
            arg_name=arg_name,
            arg_annotation=typing.get_args(arg_annotation)[0],
            arg_settings=arg_settings,
            arg_kind=arg_kind,
        )
        return UniqueMutableSequenceCutter(typevar_cutter)

    # FrozenSet
    elif typing.get_origin(arg_annotation) is frozenset:
        typevar_cutter = _resolve_cutter(
            arg_name=arg_name,
            arg_annotation=typing.get_args(arg_annotation)[0],
            arg_settings=arg_settings,
            arg_kind=arg_kind,
        )
        return UniqueImmutableSequenceCutter(typevar_cutter)

    # Literal
    elif typing.get_origin(arg_annotation) is typing.Literal:
        return LiteralCutter(*typing.get_args(arg_annotation))

    elif typing.get_origin(arg_annotation) is Mention:
        return MentionCutter(typing.get_args(arg_annotation)[0])

    elif typing.get_origin(arg_annotation) in {
        UserID,
        GroupID,
        PageID,
        User,
        Group,
        Page,
    } or arg_annotation in {
        UserID,
        GroupID,
        PageID,
        User,
        Group,
        Page,
    }:
        return EntityCutter(arg_annotation)

    else:
        raise TypeError(f"Can't resolve cutter from argument `{arg_name}`")
