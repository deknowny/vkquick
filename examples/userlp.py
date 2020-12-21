import asyncio
import os

import vkquick as vq


async def main():
    api = vq.API(os.getenv("VKDEVUSERTOKEN"))
    vq.current.curs._api = api
    lp = vq.UserLongPoll()
    await lp.setup()
    async for events in lp:
        print(events)


asyncio.run(main())