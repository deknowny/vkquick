"""
In process
"""
# import copy
#
# import vkquick_old2 as vq
# import pytest
#
# import tests_old.events as events
#
#
# @pytest.mark.asyncio
# async def test_payload_users():
#     user_id = 1
#     event = copy.deepcopy(
#         events.SIMPLE_MESSAGE
#     )
#
#     event.object.message.from_id = user_id
#
#     # Custom
#     user = await vq.User(user_id=user_id).get_info(
#         "bdate", name_case="acc"
#     )
#
#     # Via Sender
#     sender = vq.Sender("bdate", name_case="acc")
#     sender = await sender.prepare(
#         argname=...,
#         event=event,
#         func=...,
#         bin_stack=...
#     )
#     assert sender.id == user.id
#     assert sender.fn == user.fn
#     assert sender.info == user.info
