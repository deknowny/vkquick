import typing as ty

from vkquick.utils import AttrDict, SafeDict


class Wrapper:
    def __init__(self, fields: ty.Union[dict, AttrDict]) -> None:
        if isinstance(fields, dict):
            fields = AttrDict(fields)
        self._fields = fields

    def __format__(self, format_spec: str) -> str:
        format_spec = format_spec.replace(">", "}")
        format_spec = format_spec.replace("<", "{")
        extra_fields = self.extra_fields_to_format()
        format_fields = {**self.fields(), **extra_fields}
        inserted_values = SafeDict(format_fields)
        return format_spec.format_map(inserted_values)

    @property
    def fields(self):
        return self._fields

    def extra_fields_to_format(self):
        return {}

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f"{cls_name}({self.fields()})"
