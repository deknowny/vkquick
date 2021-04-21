import json

import pygments.formatters
import pygments.lexers


def pretty_view(mapping: dict, /) -> str:
    """

    Args:
      mapping:

    Returns:

    """
    dumped_mapping = json.dumps(mapping, ensure_ascii=False, indent=4)
    pretty_mapping = pygments.highlight(
        dumped_mapping,
        pygments.lexers.JsonLexer(),  # noqa
        pygments.formatters.TerminalFormatter(bg="light"),  # noqa
    )
    return pretty_mapping
