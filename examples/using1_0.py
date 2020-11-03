import os
import asyncio

import vkquick as vq


async def main():
    vq.curs.api = vq.API(os.getenv("VKDEVGROUPTOKEN"))
    lp = vq.GroupLongPoll()
    await lp.setup()
    async for events in lp:
        for event in events:
            print(event.pretty_view())


asyncio.run(main())