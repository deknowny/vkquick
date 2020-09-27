"""
Базовый класс для UI элементов
"""
import json


class UI:
    """
    Добавляет возможность vk ui _инкапсуляторам_
    (клаиватуры, карусели...)
    возможнсть генерации по словарю (напрямую в JSON)
    и саму конвертацию через `__repr__`
    """

    info: dict

    def __repr__(self) -> str:
        """
        Create for sending
        """
        return json.dumps(self.info, ensure_ascii=False)

    @classmethod
    def by(cls, pre_json: dict):
        """
        Инициализация по словарю (JSON схеме, описанной ВК)
        """
        self = object.__new__(cls)
        self.info = pre_json
        return self
