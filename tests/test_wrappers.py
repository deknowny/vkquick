import pytest
import pytest_mock
import vkquick as vq
import vkquick.wrappers.user


class TestWrapper:

    def test_repr(self):
        wrapper = vq.Wrapper({"foo": "bar"})
        assert repr(wrapper) == "Wrapper({'foo': 'bar'})"

    def test_extra_fields(self):
        assert vq.Wrapper({})._extra_fields_to_format() == {}


class TestUser:

    def test_formatting(self):
        fields = {
            "id": 1, "first_name": "a", "last_name": "b"
        }
        user = vq.User(fields)
        autoformat_mention = user.mention()
        mention_with_fields = user.mention("<fn> <ln>")
        mention_via_format = format(user, "@<fn> <ln>")
        assert autoformat_mention == mention_with_fields == mention_via_format =="[id1|a b]"

    def test_str(self):
        fields = {
            "id": 1, "first_name": "a", "last_name": "b"
        }
        user = vq.User(fields)
        assert str(user) == "<User id=1, fn='a', ln='b'>"

    @pytest.mark.asyncio
    async def test_get_registration_date(self, mocker: pytest_mock.MockerFixture):
        mocked_date_getter = mocker.patch.object(
            vkquick.wrappers.user, "get_user_registration_date"
        )
        user = vq.User({"id": 1})
        await user.get_registration_date()
        mocked_date_getter.assert_called_once_with(1, session=None)


class TestMessage:
    def test_fields(self):
        fields = {
            "date": 1,
            "from_id": 1,
            "id": 1,
            "out": 1,
            "peer_id": 1,
            "text": "hi",
            "conversation_message_id": 1,
            "fwd_messages": [],
            "important": True,
            "random_id": 1,
            "attachments": [
                {"type": "photo", "photo": {}},
                {"type": "photo", "photo": {}},
                {"type": "doc", "doc": {}}
            ],
            "is_hidden": True,
            "geo": {},
            "keyboard": "{}",
            "payload": '{"a":1}',
            "reply_message": {}
        }
        message = vq.Message(fields)
        assert message.id == message.from_id == message.peer_id == message.cmid == message.random_id == 1
        assert message.date.timestamp() == 1
        assert isinstance(message.out, bool) and message.out
        assert isinstance(message.is_hidden, bool) and message.is_hidden
        assert isinstance(message.important, bool) and message.important
        assert message.keyboard() == {}
        assert len(message.attachments) == 3
        assert message.action is message.ref is message.ref_source is message.expire_ttl is None
        assert isinstance(message.reply_message, vq.Message)
        assert len(message.photos) == 2
        assert len(message.docs) == 1
        assert message.geo == {}
        assert len(message.fwd_messages) == 0
        assert message.payload == {"a": 1}

        message = vq.Message({})
        assert message.keyboard is message.reply_message is message.payload is None