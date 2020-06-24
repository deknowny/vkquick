"""
Поднимаются от некорректного API запроса
"""
from __future__ import annotations
from typing import Tuple, Dict, Any


class VkErr(Exception):
    """
    Исключение, вызывается если VK API вернул ошибку в ответе
    """
    def __init__(self, err_info: VkErrPreparing):
        self.info = err_info


class VkErrPreparing:
    """
    Подготавливает __поля__ из ответа для ошибки
    """

    def __init__(self, err: Dict[str, Any]):
        info = self._prepare(err)
        self.text, self.code, self.msg, self.params = info

    def _prepare(self, err: Dict[str, Any]) -> Tuple[str, str, int, Dict[str, Any]]:
        error_msg = err["error"]["error_msg"]
        error_code = err["error"]["error_code"]
        error_params = err["error"]["request_params"]

        content = f"\n\n\033[31m[{error_code}] \
            {error_msg}\033[0m\n" "Request params:"
        for pair in err["error"]["request_params"]:
            key = f"\n\033[33m{pair['key']}\033[0m"
            value = f"\033[36m{pair['value']}\033[0m"
            content += f"{key} = {value}"

        return content, error_msg, error_code, error_params

    def __str__(self):
        return self.text
