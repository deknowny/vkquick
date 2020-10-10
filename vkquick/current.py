"""
Хранит специальные current-объекты.
Такие объекты представляют собой любой инстанс (например, `API` или `LongPoll`),
благодаря этому модулю находящиеся в "глобальной" для всех области видимости
"""
import typing as ty


objects: ty.Dict[str, ty.Any] = {}
"""
Место хранения current-объектов
"""


def fetch(*values_name: str) -> ty.Any:
    """
    Возвращает `property` для получения одного
    из перечисленных в `*values_names` current-объектов.
    В случае отсутствия поднимает ошибку `NameError`.

    Используйте как дескриптор.
    """

    @property
    def get_current_object(_) -> ty.Any:
        for value_name in values_name:
            # Морж смотрится не элегантно
            value = objects.get(value_name)
            if value is not None:
                return value
        else:
            raise NameError(f"No any object with names `{values_name}`")

    return get_current_object
