import dataclasses
import inspect
import typing

from vkquick.chatbot.storages import NewMessage


@dataclasses.dataclass
class Depends:
    callback: typing.Optional[
        typing.Callable[[NewMessage], typing.Any]
    ] = None


class ArgumentDependency(typing.NamedTuple):
    name: typing.Optional[str]
    handler: Depends


class DependencyMixin:
    def __init__(self):
        self._dependencies: typing.List[ArgumentDependency] = []

    def parse_dependency_arguments(self, func: typing.Callable) -> None:
        parameters = inspect.signature(func).parameters
        for name, argument in parameters.items():
            if isinstance(argument.default, Depends):
                if argument.default.callback is None:
                    argument.default.callback = argument.annotation
                self._dependencies.append(
                    ArgumentDependency(name=name, handler=argument.default)
                )

    async def make_dependency_arguments(
        self, ctx: NewMessage
    ) -> typing.Dict[str, typing.Any]:
        prepared_mapping = {}
        for dependency in self._dependencies:
            argument_value = dependency.handler.callback(ctx)
            if inspect.isawaitable(argument_value):
                await argument_value
            if dependency.name is not None:
                prepared_mapping[dependency.name] = argument_value

        return prepared_mapping
