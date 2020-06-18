from dataclasses import dataclass
from random import randint
from typing import Optional, List


class Message:
    """
    Return a message in your command
    with full `messages.send` parameters
    """
    message: Optional[int] = None
    peer_id: Optional[int] = None
    random_id: Optional[int] = None
    user_id: Optional[int] = None
    domain: Optional[str] = None
    chat_id: Optional[int] = None
    user_ids: Optional[List[int]] = None
    lat: Optional[float] = None
    long: Optional[float] = None
    attachment: Optional[List[str]] = None
    reply_to: Optional[int] = None
    forward_messages: Optional[List[int]] = None
    sticker_id: Optional[int] = None
    group_id: Optional[int] = None
    keyboard: Optional[str] = None
    payload: Optional[str] = None
    dont_parse_links: Optional[bool] = None
    disable_mentions: Optional[bool] = None
    intent: Optional[str] = None
    expire_ttl: Optional[int] = None
    silent: Optional[bool] = None


    def params(self):
        """
        Returns params for `messages.send`.
        Filters and gets without None in values
        """
        return dict(
            filter(
                lambda x: x[1] is not None, self.__dict__.items()
            )
        )

    def _set_path(self):
        """
        Chooses should be `peer_id` default or not
        """
        if not all([
            self.user_id,
            self.domain,
            self.chat_id,
            self.user_ids
        ]):
            self.peer_id = Ellipsis
