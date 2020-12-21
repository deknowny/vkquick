import asyncio
import os

import vkquick as vq
import vk_api
import vk_api.bot_longpoll


@vq.Command(names=["hello"])
def hello(sender: vq.User):
    return "hi!"



api = vk_api.VkApi(token=os.getenv("VKDEVGROUPTOKEN"))
vq.curs._api = vq.API(api.token["access_token"])
longpoll = vk_api.bot_longpoll.VkBotLongPoll(api, os.getenv("VKDEVGROUPID"))
loop = asyncio.get_event_loop()


for event in longpoll.listen():
    event = vq.Event(event.raw)
    if event.type == "message_new":
        loop.run_until_complete(hello.handle_event(event))
        pending = asyncio.all_tasks(loop)
        if pending:
            loop.run_until_complete(asyncio.wait(pending))
