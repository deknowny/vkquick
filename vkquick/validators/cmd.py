"""
Валидатор для пользвоательской текстовой команды
"""
from typing import List
from typing import Optional
import re

from .base import Validator
from vkquick import Reaction
import vkquick as vq
from vkquick import tools
from vkquick.annotypes.command_types import Optional as CmdOptional


class _SafeDict(dict):
    """
    For formatting
    """

    def __missing__(self, key):
        return f"{{{key}}}"


class Cmd(Validator):
    """
    Декоратор реакции для валидации
    пользоватлеьской команды по тексту из ```event.object.message.text```

    ## Параметры
    * `prefs`: Возможные префиксы для текстовой команды

    * `names`: Имена команды. Следуют сразу за префиксом (без пробела)

    * `sensetive`: Для True -- чувствительный к регистру символов

    * `argline`: По умолчанию все аргументы команды разделяются `\s+`,
    но вы можете создать свою _кастомную_ строку для аргументов
    (которая поддерживает регулярные выражения),
    обозначая сами аргументы {внутри фигурных скобок} и
    передавая имена этих аргументов
    в аргументы функции, в аннотациях обозначая тип.
    Например команду

    ```python
    @vq.Cmd(names=["hello"], argline="::{name}")
    @vq.Reaction("message_new")
    def hello(name: vq.Word()):
        return f"Hello, {name}!"
    ```

    можно вызвать следующим образом:


    * `hello::Bob` -> `Hello, Bob!`
    * `hello::Tom` -> `Hello, Tom!`
    * `hello::Ann` -> `Hello, Ann!`


    Если же убрать параметр argline, то команда вызывается так:


    * `hello Bob` -> `Hello, Bob!`
    * `hello Tom` -> `Hello, Tom!`
    * `hello Ann` -> `Hello, Ann!`


    `argline` воспринимается как регулярное выражение, поэтому, например, вместо
    `argline="++{name}"`
    нужно писать
    `argline="\+\+{name}"`
    потому что `+` -- это квантификатор
    """

    def __init__(
        self,
        *,
        prefs: Optional[List[str]] = None,
        names: Optional[List[str]] = None,
        argline: Optional[str] = None,
        sensetive: bool = False,
    ):
        self.prefs = [] if prefs is None else prefs
        self.names = [] if names is None else names
        self.sensetive = sensetive
        self.argline = argline
        self.regexp = ""

        self._custom_validate_annotypes = set()
        self.command_args = {}

    def _build_regexp_head(self) -> str:
        regexp = ""
        for regexp_parts in (self.prefs, self.names):
            if not regexp_parts:
                regexp_part = ""
            elif len(regexp_parts) == 1:
                regexp_part = regexp_parts[0]
            else:
                regexp_part = f"(?:{'|'.join(regexp_parts)})"

            regexp += regexp_part

        return regexp

    def _build_regexp_annotypes(self) -> str:
        regexp = ""
        for name, cmd_type in self.command_args.items():
            if not cmd_type.has_custom_validate_method():
                reaction_regexp = cmd_type.regexp
            else:
                reaction_regexp = r".*"

            regexp += rf"\s+(?P<{name}>{reaction_regexp})"

        return regexp

    def _build_regexp_argline_format(self) -> str:
        name_to_regexp = _SafeDict(
            {
                name: f"(?P<{name}>{command_type.regexp})"
                for name, command_type in self.command_args.items()
             }
        )
        return self.argline.format_map(name_to_regexp)

    def set_command_args(self, args):
        for name, value in args.items():
            cmd_type = Reaction.convert(value)

            if cmd_type.has_custom_validate_method():
                self._custom_validate_annotypes.add(name)

            self.command_args[name] = cmd_type

    def build_regexp(self) -> str:
        regexp = self._build_regexp_head()

        if self.argline:
            regexp += self._build_regexp_argline_format()
        else:
            regexp += self._build_regexp_annotypes()

        return regexp

    def __call__(self, reaction):
        self.set_command_args(reaction.command_args)

        self.regexp = self.build_regexp()
        super().__call__(reaction)
        return reaction

    def match_regexp(self, value):
        matched = (
            re.fullmatch(self.regexp, value)
            if self.sensetive
            else re.fullmatch(
                self.regexp, value, flags=re.IGNORECASE
            )
        )
        return matched

    def validate(self, event) -> None:
        text = event.object.message.text

        matched = self.match_regexp(text)

        if not matched:
            raise ValueError("Value not matched!")

        for cmd_type_with_custom_validation in self._custom_validate_annotypes:
            self._validate_custom_type(cmd_type_with_custom_validation)

        self.matched = matched

    def _validate_custom_type(self, cmd_type_name):
        raw_value = self.matched.group(cmd_type_name)
        cmd_type = self.command_args[cmd_type_name]
        cmd_type.validate(raw_value)

    async def collect(self) -> dict:
        result = {}

        for name, cmd_argument in self.command_args.items():
            raw_value = self.matched.group(name)

            cmd_instance = await tools.run(cmd_argument.build(raw_value))
            result[name] = cmd_instance

        return result
