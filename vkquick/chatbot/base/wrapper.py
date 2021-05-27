import typing


class SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


class Wrapper:
    def __init__(self, fields: dict) -> None:
        self._fields = fields

    @classmethod
    def from_kwargs(cls, **kwargs):
        return cls(kwargs)

    def __format__(self, format_spec: str) -> str:
        format_spec = format_spec.replace("]", "}")
        format_spec = format_spec.replace("[", "{")
        extra_fields = self._extra_fields_to_format()
        format_fields = {**self._fields, **extra_fields}
        inserted_values = SafeDict(format_fields)
        return format_spec.format_map(inserted_values)

    @property
    def fields(self) -> dict:
        return self._fields

    def _extra_fields_to_format(self) -> dict:
        return {}

    def __getitem__(self, item: str) -> typing.Any:
        return self._fields[item]

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f"{cls_name}({self._fields})"
