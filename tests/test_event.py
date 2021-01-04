import pytest
import vkquick as vq
import pytest_mock


def test_group_fields(make_message_new_event):

    event = make_message_new_event()

    assert event.type == "message_new"
    assert event.from_group
    assert event.event_id == event()["event_id"]
    assert str(event) == "Event(type='message_new')"

    user_event = vq.Event([4, event.event_id])
    assert user_event == event
    assert user_event.type == 4
    user_event.set_message(vq.AttrDict({}))
    assert user_event.msg.fields() == {}
    assert not user_event.from_group

    other_event = vq.Event([5, event.event_id])

    with pytest.raises(TypeError):
        other_event.set_message(None)
        other_event.msg

    old_message = event.msg
    event.object = event.object.message
    assert old_message.fields() == event.msg.fields()
