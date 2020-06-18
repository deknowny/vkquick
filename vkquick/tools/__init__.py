from .message import Message


PEER = int(2e9)


def random_id(side: int = 2**31):
    """
    Random int between +-`side` parametr.
    Use for messages.send or Message class
    """
    return randint(-side, +side)
