import dataclasses
import typing


@dataclasses.dataclass
class BadArgumentError(Exception):
    description: str


class StopCurrentHandling(Exception):
    ...


class StopStateHandling(Exception):
    def __init__(self, value: typing.Any = None, **payload):
        self.payload = value or payload
