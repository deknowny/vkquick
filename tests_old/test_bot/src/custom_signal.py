import vkquick as vq

from tests.test_bot.src._add_cache import cache


@vq.Signal("custom_signal")
def custom_signal(some_arg=False):
    """
    Handler to signal `custom_signal`
    """
    if some_arg:
        cache("custom_signal")
