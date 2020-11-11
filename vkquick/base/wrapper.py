import dataclasses
import typing as ty

import pydantic

import vkquick.utils


class Wrapper(pydantic.BaseModel):

    def __format__(self, format_spec: str) -> str:
        format_spec = format_spec.replace(">", "}")
        format_spec = format_spec.replace("<", "{")
        inserted_values = vkquick.utils.SafeDict(
            self.dict()
        )
        return format_spec.format_map(inserted_values)
