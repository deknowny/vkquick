import dataclasses


@dataclasses.dataclass
class BadArgumentError(Exception):
    description: str


class FilterFailedError(Exception):
    ...
