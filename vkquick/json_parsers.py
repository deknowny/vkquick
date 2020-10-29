import functools
import json

import vkquick.base.json_parser


class BuiltinJSONParser(vkquick.base.json_parser.JSONParser):
    """
    JSON парсер, использующий стандартную библиотеку
    """

    dumps = staticmethod(
        functools.partial(
            json.dumps, ensure_ascii=False, separators=(",", ":")
        )
    )
    loads = staticmethod(json.loads)
