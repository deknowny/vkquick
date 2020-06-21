import asyncio
import ssl
import time
import re
import logging
from typing import Dict
from typing import Any
from dataclasses import dataclass

import aiohttp
import attrdict
import colorama

from . import exception as ex
from .annotypes import Annotype


# colorama.init(reset=True)
colorama.init()


@dataclass
class API:
    """
    Send API requests
    """

    token: str
    version: float
    delay: float = 1/20

    def __post_init__(self):
        self.URL: str = "https://api.vk.com/method/"

        self._method = str()
        self._last_request_time = 0

    def __getattr__(self, attr) -> "self":
        """
        Build a method name
        """
        pycase = re.findall(r"_([a-z])", attr)
        for low in pycase:
            attr.replace(f"_{low}", low.upper())
        if self._method:
            self._method += f".{attr}"
        else:
            self._method = attr
        return self

    def __call__(self, **kwargs):
        """
        Called after dot-getting
        """
        meth_name = self._method
        self._method = str()
        result = self.method(name=meth_name, data=kwargs)
        return result

    @staticmethod
    def prepare(argname, event, func, bot, bin_stack):
        return bot.api

    async def method(self, name: str, data):
        await self._waiting()
        data.update(access_token=self.token, v=self.version)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=self.URL + name, data=data, ssl=ssl.SSLContext()
            ) as response:
                response = await response.json()
                self._check_errors(response)
                if isinstance(response["response"], dict):
                    return attrdict.AttrMap(response["response"])
                return response["response"]

    def _check_errors(self, resp: Dict[str, Any]) -> None:
        if "error" in resp:
            raise ex.VkErr(ex.VkErrPreparing(resp))

    async def _waiting(self):
        diff = time.time() - self._last_request_time
        if diff < self.delay:
            wait_time = self.delay - diff
            self._last_request_time += self.delay
            await asyncio.sleep(wait_time)


class APIMerging:
    """
    Merge API instance to your class.
    Use to get private parametrs like
    token, group_id and etc or easily
    make async API requests
    """

    def merge(self, api: API) -> "self":
        """
        Merge API instance to class for adding
        API requests abilities
        """
        if not isinstance(api, API):
            raise NotImplementedError()
        self._api = api
        return self

    @property
    def api(self):
        """
        API instance
        """

    @api.getter
    def api(self) -> API:
        # if self._api is None:
        #     raise ValueError(
        #         f"vkdev.API hasn't been merged "
        #         f"for instance of class `{self.__class__}`. "
        #         "Pass it by setting `api` attribute or "
        #         "pass it into `.add()` or "
        #         "add `API` instance by __radd__ (also works `__add__`) ",
        #         "for example:\n"
        #         f"hand = API('token') + {self.__class__}()\n"
        #         f"{self.__class__}().add(API('token'))"
        #     )
        return self._api

    @api.setter
    def api(self, inst: API):
        self._api = inst
