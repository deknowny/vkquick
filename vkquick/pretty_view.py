import json

import pygments.formatters
import pygments.lexers


def pretty_view(__mapping: dict) -> str:
    dumped_mapping = json.dumps(__mapping, ensure_ascii=False, indent=4)
    pretty_mapping = pygments.highlight(
        dumped_mapping,
        pygments.lexers.JsonLexer(),
        pygments.formatters.TerminalFormatter(bg="light"),
    )
    return pretty_mapping
