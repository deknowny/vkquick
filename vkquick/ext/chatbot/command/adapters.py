from __future__ import annotations

import inspect
import typing as ty

from vkquick.ext.chatbot.base.cutter import (
    Argument,
    CommandTextArgument,
    TextCutter,
)
from vkquick.ext.chatbot.command.cutters import (
    MentionCutter,
    IntegerCutter,
    FloatCutter,
    StringCutter,
    WordCutter,
    OptionalCutter,
    UnionCutter,
    MutableSequenceCutter,
    ImmutableSequenceCutter,
    GroupCutter,
    UniqueMutableSequenceCutter,
    UniqueImmutableSequenceCutter,
    LiteralCutter,
    Mention,
    UserID,
    GroupID,
    PageID,
    EntityCutter,
)
from vkquick.ext.chatbot.providers.page import (
    UserProvider,
    GroupProvider,
    PageProvider,
)
from vkquick.ext.chatbot.wrappers.page import User, Group, Page
from vkquick.ext.chatbot_old.wrappers import User, Group, Page


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
        and not ty.get_origin(parameter.annotation) is ty.Union
    ):
        arg_annotation = ty.Optional[parameter.annotation]
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
    *, arg_name: str, arg_annotation: ty.Any, arg_settings: Argument, arg_kind
) -> TextCutter:

    if arg_annotation is int:
        return IntegerCutter()
    elif arg_annotation is float:
        return FloatCutter()
    elif arg_annotation is str:
        if arg_kind == inspect.Parameter.KEYWORD_ONLY:
            return StringCutter()
        else:
            return WordCutter()

    # Optional
    elif ty.get_origin(arg_annotation) is ty.Union and type(
        None
    ) in ty.get_args(arg_annotation):
        return OptionalCutter(
            _resolve_cutter(
                arg_name=arg_name,
                arg_annotation=ty.get_args(arg_annotation)[0],
                arg_settings=arg_settings,
                arg_kind=arg_kind,
            ),
            default=arg_settings.default,
            default_factory=arg_settings.default_factory,
        )
    # Union
    elif ty.get_origin(arg_annotation) is ty.Union:
        typevar_cutters = (
            _resolve_cutter(
                arg_name=arg_name,
                arg_annotation=typevar,
                arg_settings=arg_settings,
                arg_kind=arg_kind,
            )
            for typevar in ty.get_args(arg_annotation)
        )
        return UnionCutter(*typevar_cutters)

    # List
    elif ty.get_origin(arg_annotation) is list:
        typevar_cutter = _resolve_cutter(
            arg_name=arg_name,
            arg_annotation=ty.get_args(arg_annotation)[0],
            arg_settings=arg_settings,
            arg_kind=arg_kind,
        )
        return MutableSequenceCutter(typevar_cutter)
    # Tuple sequence
    elif ty.get_origin(arg_annotation) is tuple and Ellipsis in ty.get_args(
        arg_annotation
    ):
        typevar_cutter = _resolve_cutter(
            arg_name=arg_name,
            arg_annotation=ty.get_args(arg_annotation)[0],
            arg_settings=arg_settings,
            arg_kind=arg_kind,
        )
        return ImmutableSequenceCutter(typevar_cutter)

    # Tuple
    elif ty.get_origin(
        arg_annotation
    ) is tuple and Ellipsis not in ty.get_args(arg_annotation):

        typevar_cutters = (
            _resolve_cutter(
                arg_name=arg_name,
                arg_annotation=typevar,
                arg_settings=arg_settings,
                arg_kind=arg_kind,
            )
            for typevar in ty.get_args(arg_annotation)
        )

        return GroupCutter(*typevar_cutters)

    # Set
    elif ty.get_origin(arg_annotation) is set:
        typevar_cutter = _resolve_cutter(
            arg_name=arg_name,
            arg_annotation=ty.get_args(arg_annotation)[0],
            arg_settings=arg_settings,
            arg_kind=arg_kind,
        )
        return UniqueMutableSequenceCutter(typevar_cutter)

    # FrozenSet
    elif ty.get_origin(arg_annotation) is frozenset:
        typevar_cutter = _resolve_cutter(
            arg_name=arg_name,
            arg_annotation=ty.get_args(arg_annotation)[0],
            arg_settings=arg_settings,
            arg_kind=arg_kind,
        )
        return UniqueImmutableSequenceCutter(typevar_cutter)

    # Literal
    elif ty.get_origin(arg_annotation) is ty.Literal:
        return LiteralCutter(*ty.get_args(arg_annotation))

    elif ty.get_origin(arg_annotation) is Mention:
        return MentionCutter(
            ty.get_args(arg_annotation)[0], **arg_settings.cutter_preferences
        )

    elif arg_annotation in {
        UserID,
        GroupID,
        PageID,
        User,
        Group,
        Page,
        UserProvider,
        GroupProvider,
        PageProvider,
    }:
        return EntityCutter(arg_annotation, **arg_settings.cutter_preferences)

    else:
        raise TypeError(f"Can't resolve cutter from argument `{arg_name}`")
