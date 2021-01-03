"""
Test filters
"""
import vkquick as vq
import pytest



def test_base_filter():
    command = vq.Command()
    filter_object1 = vq.Action("123")
    filter_object2 = vq.Enable()
    filter_object1(command)
    filter_object2(command)
    assert command.filters == [command, filter_object1, filter_object2]


def test_chat_only(make_message_new_event):
    filter = vq.ChatOnly()
    event = make_message_new_event()
    event.msg._fields["peer_id"] = 1
    ctx = vq.Context(event=event, shared_box=None)
    assert not filter.make_decision(ctx).passed
    event.msg._fields["peer_id"] = vq.peer(1)
    assert filter.make_decision(ctx)


def test_direct_only(make_message_new_event):
    filter = vq.DirectOnly()
    event = make_message_new_event()
    event.msg._fields["peer_id"] = 1
    ctx = vq.Context(event=event, shared_box=None)
    assert filter.make_decision(ctx).passed
    event.msg._fields["peer_id"] = vq.peer(1)
    assert not filter.make_decision(ctx).passed


def test_ignore_bots_messages(make_message_new_event):
    filter = vq.IgnoreBotsMessages()
    event = make_message_new_event()
    event.msg._fields["from_id"] = -1
    ctx = vq.Context(event=event, shared_box=None)
    assert not filter.make_decision(ctx).passed
    event.msg._fields["from_id"] = 1
    assert filter.make_decision(ctx).passed

# class TestEnable:
#     def test_init(self):
#         inst = vq.Enable()
#         assert inst.enabled
#         inst = vq.Enable(False)
#         assert not inst.enabled
#
#     def test_passed_decision(self):
#         inst_enabled = vq.Enable()
#         event = vq.Event({})
#         decision = inst_enabled.make_decision(event)
#         assert decision == (True, inst_enabled.passed_decision)
#
#     def test_not_passed_decision(self):
#         inst_disable = vq.Enable(False)
#         event = vq.Event({})
#         decision = inst_disable.make_decision(event)
#         assert decision == (False, inst_disable.not_passed_decision)
