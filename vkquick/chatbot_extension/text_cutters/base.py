from __future__ import annotations

import abc
import typing as ty


class CutterResponse(ty.NamedTuple):
    remain_string: str
    parsed_value: ty.Any


class TextCutter(abc.ABC):
    @abc.abstractmethod
    def cut_part(self, arguments_string: str) -> CutterResponse:
        ...
