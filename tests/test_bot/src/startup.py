import vkquick as vq

from ._add_cache import cache


@vq.Signal("startup")
def startup():
    """
    Handler to signal `startup`
    """
    cache("startup")
