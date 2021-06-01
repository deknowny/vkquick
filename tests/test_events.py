import vkquick as vq


def test_group_event():
    event_content = {
        "type": "message_new",
        "object": {"text": "abc"},
        "group_id": 1,
    }
    event = vq.GroupEvent(event_content)
    assert event.content == event_content
    assert event.object == event_content["object"]
    assert event.group_id == 1
    assert event.type == "message_new"


def test_user_event():
    event_content = [4, 123, 123]
    event = vq.UserEvent(event_content)
    assert event.content == event_content == event.object == event_content
    assert event.type == 4
