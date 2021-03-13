"""
Test `api.py` module
"""
import re

import aiohttp
import pytest
import pytest_mock
import vkquick as vq

import unittest.mock


class TestAPI:
    @pytest.mark.asyncio
    async def test_getattr(self, mocker: pytest_mock.MockerFixture):
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        api._convert_name = mocker.MagicMock(return_value="foo.bar")
        api._make_api_request = mocker.AsyncMock()
        await api.users.get()
        await api.some.other()
        await api.foo.bar()

        calls = [
            mocker.call("users.get"),
            mocker.call("some.other"),
            mocker.call("foo.bar"),
        ]

        api._convert_name.assert_has_calls(calls)

    @pytest.mark.asyncio
    async def test_autocomplete_params(
        self, mocker: pytest_mock.MockerFixture
    ):
        api = vq.API(
            "token",
            token_owner=vq.TokenOwner.GROUP,
            autocomplete_params={"foo": "bar"},
        )
        api._make_api_request = mocker.AsyncMock()
        await api.foo.bar()
        await api.foo.bar(...)
        calls = [
            mocker.call(
                method_name=mocker.ANY,
                request_params={"access_token": api.token, "v": api.version},
                allow_cache=mocker.ANY,
            ),
            mocker.call(
                method_name=mocker.ANY,
                request_params={
                    "access_token": api.token,
                    "foo": "bar",
                    "v": api.version,
                },
                allow_cache=mocker.ANY,
            ),
        ]
        api._make_api_request.assert_has_calls(calls)

    @pytest.mark.asyncio
    async def test_call_via_method(self, mocker: pytest_mock.MockerFixture):
        api = vq.API(
            "token",
            token_owner=vq.TokenOwner.GROUP,
            autocomplete_params={"foo": "bar"},
        )
        api._make_api_request = mocker.AsyncMock()
        await api.method("foo.bar", {"a": 1})
        api._make_api_request.assert_called_once_with(
            method_name="foo.bar",
            request_params={
                "access_token": api.token,
                "a": "1",
                "v": api.version,
            },
            allow_cache=False,
        )

    @pytest.mark.parametrize(
        "params,output",
        [
            ({"foo": "bar"}, {"foo": "bar"}),
            ({"foo": ["fizz", "bazz"]}, {"foo": "fizz,bazz"}),
            (
                {"list": [1, 2], "int": 1, "tuple": (1, 2), "set": {1, 2}},
                {"list": "1,2", "int": "1", "tuple": "1,2", "set": "1,2"},
            ),
            ({"foo": {"a": 1}}, {"foo": '{"a":1}'}),
            (
                {"foo": vq.Keyboard().build()},
                {"foo": vq.Keyboard().build().represent_as_api_param()},
            ),
            ({"foo": True}, {"foo": 1}),
            ({"foo": None}, {}),
        ],
    )
    def test_convert_params(self, params, output):
        new_params = vq.API._convert_params_for_api(params)
        assert new_params == output

    def test_build_cache_hash(self, mocker: pytest_mock.MockerFixture):
        mocked_parser = mocker.patch(
            "urllib.parse.urlencode", return_value="a"
        )
        assert vq.API._build_cache_hash("foo", {}) == "foo#a"
        mocked_parser.return_value = "b"
        assert vq.API._build_cache_hash("bar", {}) == "bar#b"

    def test_prepare_response_body(self, mocker: pytest_mock.MockerFixture):
        mocked_exception = mocker.patch.object(
            vq.VKAPIError, "destruct_response", return_value=Exception()
        )
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        api._prepare_response_body({"response": 1})
        mocked_exception.assert_not_called()
        with pytest.raises(Exception):
            api._prepare_response_body({"error": 0})
        mocked_exception.assert_called_once()

    @pytest.mark.asyncio
    async def test_make_async_api_request(
        self, mocker: pytest_mock.MockerFixture
    ):
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        api._send_api_request = mocker.AsyncMock(
            return_value={"response": 1}
        )
        request = await api.users.get(foo=1)
        api._send_api_request.assert_called_once_with(
            path="users.get",
            params={"access_token": api.token, "foo": "1", "v": api.version,},
        )
        assert request == 1

    @pytest.mark.asyncio
    async def test_make_cached_async_api_request(
        self, mocker: pytest_mock.MockerFixture
    ):
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        api._build_cache_hash = mocker.Mock(return_value="a")
        api._send_api_request = mocker.AsyncMock(
            return_value={"response": 1}
        )
        request1 = await api.users.get(foo=1, allow_cache_=True)
        request2 = await api.users.get(foo=1, allow_cache_=True)
        api._send_api_request.assert_called_once_with(
            path="users.get",
            params={"access_token": api.token, "foo": "1", "v": api.version,},
        )
        assert api._build_cache_hash.call_count == 2
        assert request1 == request2 == 1 == api.cache_table["a"]

    @pytest.mark.asyncio
    async def test_sending_async_api_request(
        self, mocker: pytest_mock.MockerFixture
    ):
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        mocker.patch("aiohttp.TCPConnector")
        session = mocker.patch("aiohttp.ClientSession", name="session")
        session.return_value = session
        response_mock = mocker.Mock()
        response_mock.json = mocker.AsyncMock(return_value={"response": 1})
        session.post = mocker.Mock(return_value=session)
        session.__aenter__ = mocker.AsyncMock(return_value=response_mock)
        session.__aexit__ = mocker.AsyncMock(return_value=response_mock)
        req1 = await api.users.get()
        assert req1 == 1
        response_mock.json.assert_called_once_with(
            loads=vq.json_parser_policy.loads
        )
        session.post.assert_called_once_with(
            f"https://api.vk.com/method/users.get",
            data={"access_token": api.token, "v": api.version},
        )
        await api.users.get()
        session.assert_called_once()

    def test_make_sync_api_request(self, mocker: pytest_mock.MockerFixture):
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        api._send_sync_api_request = mocker.Mock(return_value={"response": 1})
        with api.synchronize():
            request = api.users.get(foo=1)
        api._send_sync_api_request.assert_called_once_with(
            path="users.get",
            params={"access_token": api.token, "foo": "1", "v": api.version,},
        )
        assert request == 1

    def test_make_cached_sync_api_request(
        self, mocker: pytest_mock.MockerFixture
    ):
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        api._build_cache_hash = mocker.Mock(return_value="a")
        api._send_sync_api_request = mocker.Mock(return_value={"response": 1})
        with api.synchronize():
            request1 = api.users.get(foo=1, allow_cache_=True)
            request2 = api.users.get(foo=1, allow_cache_=True)
        api._send_sync_api_request.assert_called_once_with(
            path="users.get",
            params={"access_token": api.token, "foo": "1", "v": api.version,},
        )
        assert api._build_cache_hash.call_count == 2
        assert request1 == request2 == 1 == api.cache_table["a"]

    def test_sending_sync_api_request(
        self, mocker: pytest_mock.MockerFixture
    ):
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        response = mocker.Mock()
        response.content = '{"response":1}'
        api.sync_http_session = mocker.Mock(name="session")
        api.sync_http_session.post = mocker.Mock(
            name="session", return_value=response
        )
        mocker.patch.object(
            vq.json_parser_policy, "loads", return_value={"response": 1}
        )

        with api.synchronize():
            req1 = api.users.get()
        assert req1 == 1
        vq.json_parser_policy.loads.assert_called_once_with(response.content)
        api.sync_http_session.post.assert_called_once_with(
            f"https://api.vk.com/method/users.get",
            data={"access_token": api.token, "v": api.version},
        )

    def test_upper_zero_group(self):
        match = re.fullmatch(r"(?P<let>foo)", "foo")
        assert vq.API._upper_zero_group(match) == "FOO"

    def test_define_token_owner(self, mocker: pytest_mock.MockerFixture):
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        api._make_api_request = mocker.MagicMock(return_value=vq.AttrDict([]))
        assert api._define_token_owner() == vq.TokenOwner.GROUP
        api._make_api_request = mocker.MagicMock(
            return_value=vq.AttrDict([{"some": "user"}])
        )
        assert api._define_token_owner() == vq.TokenOwner.USER

    @pytest.mark.asyncio
    async def test_close_session(self, mocker: pytest_mock.MockerFixture):
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        api.async_http_session = mocker.Mock()
        api.async_http_session.close = mocker.AsyncMock()
        await api.close_session()
        api.async_http_session.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_fetch_user_via_id(
        self, mocker: pytest_mock.MockerFixture
    ):
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        api._make_api_request = mocker.AsyncMock(
            return_value=vq.AttrDict([{"foo": 1}])
        )
        user = await api.fetch_user_via_id(1)
        assert user.fields() == {"foo": 1}

    def test_fetch_user_via_id(self, mocker: pytest_mock.MockerFixture):
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        api._make_api_request = mocker.Mock(
            return_value=vq.AttrDict([{"foo": 1}])
        )
        with api.synchronize():
            user = api.fetch_user_via_id(1)
        assert user.fields() == {"foo": 1}

    @pytest.mark.asyncio
    async def test_async_fetch_user_via_ids(
        self, mocker: pytest_mock.MockerFixture
    ):
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        infos = [{"foo": 1}, {"foo": 2}, {"foo": 3}]
        api._make_api_request = mocker.AsyncMock(
            return_value=vq.AttrDict([{"foo": 1}, {"foo": 2}, {"foo": 3}])
        )
        users = await api.fetch_users_via_ids([1, 2, 3])
        for user, info in zip(users, infos):
            assert isinstance(user, vq.User)
            assert info == user.fields()

    def test_sync_fetch_user_via_ids(self, mocker: pytest_mock.MockerFixture):
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        infos = [{"foo": 1}, {"foo": 2}, {"foo": 3}]
        api._make_api_request = mocker.Mock(
            return_value=vq.AttrDict([{"foo": 1}, {"foo": 2}, {"foo": 3}])
        )
        with api.synchronize():
            users = api.fetch_users_via_ids([1, 2, 3])
        for user, info in zip(users, infos):
            assert isinstance(user, vq.User)
            assert info == user.fields()

    @pytest.mark.asyncio
    async def test_init_lp(self):
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        group_lp = api.init_group_lp()
        assert isinstance(group_lp, vq.GroupLongPoll)
        api = vq.API("token", token_owner=vq.TokenOwner.USER)
        user_lp = api.init_user_lp()
        assert isinstance(user_lp, vq.UserLongPoll)


def test_token_owner():
    assert vq.TokenOwner.GROUP == "group"
    assert vq.TokenOwner.USER == "user"
