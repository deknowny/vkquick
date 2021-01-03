import pytest
import pytest_mock
import vkquick as vq
import vkquick.wrappers.user


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
