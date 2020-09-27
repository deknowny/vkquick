import vkquick as vq

from ._add_cache import cache


@vq.Signal("shutdown")
def shutdown():
    """
    Handler to signal `shutdown`
    """
    cache("shutdown")
