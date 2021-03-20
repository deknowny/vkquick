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
        fields = {"id": 1, "first_name": "a", "last_name": "b"}
        user = vq.User(fields)
        autoformat_mention = user.mention()
        mention_with_fields = user.mention("<fn> <ln>")
        mention_via_format = format(user, "@<fn> <ln>")
        assert (
            autoformat_mention
            == mention_with_fields
            == mention_via_format
            == "[id1|a b]"
        )

    def test_str(self):
        fields = {"id": 1, "first_name": "a", "last_name": "b"}
        user = vq.User(fields)
        assert str(user) == "<User id=1, fn='a', ln='b'>"

    @pytest.mark.asyncio
    async def test_get_registration_date(
        self, mocker: pytest_mock.MockerFixture
    ):
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
            "peer_id": vq.peer(1),
            "text": "hi",
            "conversation_message_id": 1,
            "fwd_messages": [],
            "important": True,
            "random_id": 1,
            "attachments": [
                {"type": "photo", "photo": {}},
                {"type": "photo", "photo": {}},
                {"type": "doc", "doc": {}},
            ],
            "is_hidden": True,
            "geo": {},
            "keyboard": "{}",
            "payload": '{"a":1}',
            "reply_message": {},
        }
        message = vq.Message(fields)
        assert (
            message.id
            == message.from_id
            == message.peer_id - vq.peer()
            == message.cmid
            == message.random_id
            == 1
        )
        assert message.date.timestamp() == 1
        assert isinstance(message.out, bool) and message.out
        assert isinstance(message.is_hidden, bool) and message.is_hidden
        assert isinstance(message.important, bool) and message.important
        assert message.keyboard() == {}
        assert len(message.attachments) == 3
        assert (
            message.action
            is message.ref
            is message.ref_source
            is message.expire_ttl
            is None
        )
        assert isinstance(message.reply_message, vq.Message)
        assert len(message.photos) == 2
        assert len(message.docs) == 1
        assert message.geo == {}
        assert len(message.fwd_messages) == 0
        assert message.payload == {"a": 1}
        assert message.chat_id == 1

        message = vq.Message({})
        assert (
            message.keyboard
            is message.reply_message
            is message.payload
            is None
        )

        with pytest.raises(ValueError):
            message = vq.Message({"peer_id": 1})
            message.chat_id


class TestPhoto:
    @pytest.mark.asyncio
    async def test_download(self, mocker):
        fields = {
            "album_id": -3,
            "date": 1609711476,
            "id": 457248699,
            "owner_id": 447532348,
            "has_tags": False,
            "access_key": "105b29bafd1831f3d3",
            "sizes": [
                {"height": 42, "url": "size-s", "type": "s", "width": 75},
                {"height": 73, "url": "size-m", "type": "m", "width": 130},
                {"height": 338, "url": "size-x", "type": "x", "width": 604},
                {"height": 436, "url": "size-y", "type": "y", "width": 780},
                {"height": 87, "url": "size-o", "type": "o", "width": 130},
                {"height": 133, "url": "size-p", "type": "p", "width": 200},
                {"height": 213, "url": "size-q", "type": "q", "width": 320},
                {"height": 340, "url": "size-r", "type": "r", "width": 510},
            ],
            "text": "",
        }
        photo = vq.Photo(fields)
        mocked_download = mocker.patch(
            "vkquick.wrappers.attachment.download_file"
        )
        await photo.download_max_size()
        await photo.download_min_size()
        await photo.download_with_size("q")

        calls = [
            mocker.call("size-r"),
            mocker.call("size-s"),
            mocker.call("size-q"),
        ]
        mocked_download.assert_has_calls(calls)

        with pytest.raises(ValueError):
            await photo.download_with_size("aaa")
