"""
Дополнительные исключения
"""
from __future__ import annotations

import dataclasses
import typing

import huepy
import jinja2
import typing_extensions as tye

exceptions_storage: typing.Dict[int, typing.Type[APIError]] = {}


class _ParamsScheme(tye.TypedDict):
    """
    Структура параметров, возвращаемых
    при некорректном обращении к API
    """

    key: str
    value: str  # Даже если в запросе было передано число, значение будет строкой


template_source = """
[{{ huepy.red(status_code) }}] {{ description -}}
{% for param in params %}
# {{ huepy.yellow(param["key"]) }} = {{ huepy.cyan(param["value"]) -}}
{% endfor %}

{% if self.extra_fields %}
{{- huepy.info("There are some extra fields:") }}
{{ extra_fields -}}
{% endif %}
"""
exception_text_template = jinja2.Template(template_source)


@dataclasses.dataclass
class APIError(Exception):
    """
    Исключение, поднимаемое при некорректном вызове API запроса.

    Arguments:
        pretty_exception_text: Красиво выстроенное сообщение с ошибкой от API
        description: Описание ошибки (из API ответа)
        status_code: Статус-код ошибки (из API ответа)
        request_params: Параметры запроса, в ответ на который пришла ошибка
        extra_fields: Дополнительные поля (из API ответа)
    """

    description: str
    status_code: int
    request_params: typing.List[_ParamsScheme]
    extra_fields: dict

    def __class_getitem__(
        cls, code: typing.Union[int, typing.Tuple[int, ...]]
    ) -> typing.Tuple[typing.Type[APIError]]:
        result_classes = []
        codes = (code,) if isinstance(code, int) else code
        for code in codes:
            if code in exceptions_storage:
                result_classes.append(exceptions_storage[code])
            else:
                new_class = type(f"APIError{code}", (APIError,), {})
                new_class = typing.cast(typing.Type[APIError], new_class)
                exceptions_storage[code] = new_class
                result_classes.append(new_class)

        return tuple(result_classes)

    def __str__(self) -> str:
        return exception_text_template.render(
            status_code=self.status_code,
            description=self.description,
            params=self.request_params,
            extra_fields=self.extra_fields,
            huepy=huepy,
        )
