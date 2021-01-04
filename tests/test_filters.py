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


def test_action(make_message_new_event):
    filter = vq.Action("extra", chat_create=True)
    event = make_message_new_event()
    event.msg._fields["action"] = {"type": "extra"}
    ctx = vq.Context(event=event, shared_box=None)
    assert filter.make_decision(ctx).passed
    event.msg._fields["action"] = {"type": "ф"}
    assert not filter.make_decision(ctx).passed
    event.msg._fields["action"] = {"type": "chat_create"}
    assert filter.make_decision(ctx).passed
    del event.msg._fields()["action"]
    assert not filter.make_decision(ctx).passed

    with pytest.raises(ValueError):
        vq.Action()


def test_allow_access_for(make_message_new_event):
    event = make_message_new_event()
    ctx = vq.Context(event=event, shared_box=None)
    filter = vq.AllowAccessFor(123)
    event.msg._fields["from_id"] = 123
    assert filter.make_decision(ctx).passed
    filter = vq.AllowAccessFor(token_owner=True)
    event.msg._fields["out"] = True
    assert filter.make_decision(ctx).passed
    event.msg._fields["out"] = False
    assert not filter.make_decision(ctx).passed

    with pytest.raises(ValueError):
        vq.AllowAccessFor()
