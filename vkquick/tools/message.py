from random import randint
from typing import Optional, List

from attrdict import AttrMap


class Message:
    """
    Return a message in your command
    with full `messages.send` parameters
    """

    def __init__(
        self,
        message: Optional[int] = None, *,
        peer_id: Optional[int] = None,
        random_id: int = 0,
        user_id: Optional[int] = None,
        domain: Optional[str] = None,
        chat_id: Optional[int] = None,
        user_ids: Optional[List[int]] = None,
        peer_ids: Optional[List[int]] = None,
        lat: Optional[float] = None,
        long: Optional[float] = None,
        attachment: Optional[List[str]] = None,
        reply_to: Optional[int] = None,
        forward_messages: Optional[List[int]] = None,
        sticker_id: Optional[int] = None,
        group_id: Optional[int] = None,
        keyboard: Optional[str] = None,
        payload: Optional[str] = None,
        dont_parse_links: Optional[bool] = None,
        disable_mentions: Optional[bool] = None,
        intent: Optional[str] = None,
        expire_ttl: Optional[int] = None,
        silent: Optional[bool] = None,
        **kwargs
    ):
        preload_data = locals().copy()
        del preload_data["self"]
        kwargs_vals = preload_data.pop("kwargs")
        preload_data.update(kwargs_vals)

        self._params = AttrMap(
            dict(
                filter(
                    lambda x: x[1] is not None, preload_data.items()
                )
            )
        )
        self._set_path()

    @property
    def params(self):
        """
        Returns params for `messages.send`.
        Filters and gets without None in values
        """
        return self._params

    def _set_path(self):
        """
        Chooses should be `peer_id` default or not
        """
        if not (
            {"user_id", "domain", "chat_id", "user_ids", "peer_ids"} &
            set(self._params)
        ):
            self._params.peer_id = Ellipsis
