from typing import Generator
from functools import wraps

from .ui import UI
from .element import Element


class Template(UI):
    """
    Карусель с элементами. Используйте в сообщении
    """

    def __init__(self, type_: str = "carousel"):
        self.info = dict(type=type_, elements=[])

    def __call__(self, gen: Generator[Element, None, None]):
        @wraps(gen)
        def wrapper(*args, **kwargs):
            for elem in gen(*args, **kwargs):
                self.info["elements"].append(elem.info)

            return self

        return wrapper
