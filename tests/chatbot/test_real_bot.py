import asyncio

import vkquick as vq
import pytest

#
# @pytest.mark.asyncio
# async def test_ping_bot(group_api, user_api):
#     ponged = False
#     peer_id = None
#
#     group_app = vq.App()
#
#     @group_app.on_startup()
#     async def startup(bot: vq.Bot):
#         nonlocal peer_id
#         _, owner = await bot.api.define_token_owner()
#         peer_id = owner.id
#
#     @group_app.command("ping")
#     async def echo():
#         return "pong"
#
#     @group_app.command("pong")
#     async def echo():
#         breakpoint()
#         return "pong"
#
#     group_bot_run_task = asyncio.create_task(
#         group_app.coroutine_run("$GROUP_TOKEN", build_autodoc=False)
#     )
#
#     user_app = vq.App()
#
#     @user_app.on_startup()
#     async def startup(bot: vq.Bot):
#         # Setup group bot
#         await asyncio.sleep(6)
#         await bot.api.method(
#             "messages.send",
#             peer_id=-peer_id,
#             message="ping",
#             random_id=vq.random_id()
#         )
#     #
#     # @user_app.command("pong")
#     # async def pong():
#     #     nonlocal ponged
#     #     ponged = True
#     #     group_bot_run_task.cancel()
#     #     user_bot_run_task.cancel()
#     #
#     #     try:
#     #         await group_bot_run_task
#     #     except asyncio.CancelledError:
#     #         pass
#     #
#     #     try:
#     #         await user_bot_run_task
#     #     except asyncio.CancelledError:
#     #         pass
#
#     user_bot_run_task = asyncio.create_task(
#         user_app.coroutine_run("$USER_TOKEN", build_autodoc=False)
#     )
#     try:
#         await asyncio.gather(
#             group_bot_run_task, user_bot_run_task
#         )
#     except asyncio.CancelledError:
#         pass
#
#     assert ponged
#
