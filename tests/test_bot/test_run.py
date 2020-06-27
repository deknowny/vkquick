import pathlib
import os
import threading

import vkquick as vq
import attrdict
import toml

from tests.test_bot.user import main_user


CACHE_SET = {
    "startup",
    "shutdown",
    "cmd_insensetive",
    "cmd_argline",
    "cmd_types",
    "com_prefs",
    "annotypes1",
    "annofwd",
    "annorep",
    "join_chat",
    "usertool",
    "custom_signal",
    "send_photo",
    "doc_uploader",
    "apireq"
}

# Create cache if not exists
open(pathlib.Path() / "tests" / "test_bot" / ".cache", "w+")

def test_bot_run(run_thread=True):
    # Bot's
    from tests.test_bot import src

    config = attrdict.AttrMap(toml.load(
            str(
                pathlib.Path() / "tests" / "test_bot" / "config.toml"
            )
        )
    )
    settings = dict(
        token=config.api.token,
        group_id=config.api.group_id,
        version=config.api.version,
        owner=config.api.owner,
        wait=config.longpoll.wait,
        debug=True,
        config=config
    )

    reactions = []
    signals = []
    for var in src.__dict__.values():
        if isinstance(var, vq.Reaction):
            reactions.append(var)
        elif isinstance(var, vq.Signal):
            signals.append(var)
    reactions = vq.ReactionsList(reactions)
    signals = vq.SignalsList(signals)

    bot = vq.Bot(
        reactions=reactions,
        signals=signals,
        **settings
    )
    if run_thread:
        thread = threading.Thread(target=main_user)
        thread.start()

    bot.run()


def test_run():
    cache_path = pathlib.Path() / "tests" / "test_bot" / ".cache"
    with open(pathlib.Path() / "tests" / "test_bot" / ".cache", "r") as cache:
        cache = set(cache.read().split())

    os.remove(cache_path)

    assert not (CACHE_SET - cache)


if __name__ == "__main__":
    test_bot_run(False)
