import dataclasses
import typing as ty

import pydantic

import vkquick.utils


class Wrapper(pydantic.BaseModel):
    def __format__(self, format_spec: str) -> str:
        format_spec = format_spec.replace(">", "}")
        format_spec = format_spec.replace("<", "{")
        extra_fields = self.extra_fields_to_format()
        format_fields = {**self.dict(), **extra_fields}
        inserted_values = vkquick.utils.SafeDict(format_fields)
        return format_spec.format_map(inserted_values)

    def extra_fields_to_format(self):
        return {}
