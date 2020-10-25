"""
Test `api.py` module
"""
import pytest
import pytest_mock
import vkquick as vq

import unittest.mock
import copy


class _ImplementedRead:
    def __init__(self, read_return_value):
        self.read_return_value = read_return_value

    def read(self):
        return self.read_return_value


class TestAPI:
    async_data_request = [
        [
            "users",
            "get",
            {"fetch": "name"},
            b"GET /method/users.get?"
            + b"access_token=token&v="
            + vq.API.version.encode("utf-8")
            + b"&fetch=name "
            + b"HTTP/1.1\n"
            + b"Host: api.vk.com\n\n",
            '{"response": {"name": "Bob"}}',
            {"name": "Bob"},
        ],
        [
            "some",
            "api_method_with_underscores",
            {"param1": [1, 2], "foo": ("egg", "spam")},
            b"GET /method/some.apiMethodWithUnderscores?"
            + b"access_token=token&v="
            + vq.API.version.encode("utf-8")
            + b"&param1=1%2C2&foo=egg%2Cspam "
            + b"HTTP/1.1\n"
            + b"Host: api.vk.com\n\n",
            '{"response": {"method": "called", "foo": [1, 2]}}',
            {"method": "called", "foo": [1, 2]},
        ],
    ]
    sync_data_request = copy.deepcopy(async_data_request)
    sync_data_request[0][3] = (
        "https://api.vk.com/method/users.get?"
        f"access_token=token&v={vq.API.version}&fetch=name"
    )
    sync_data_request[1][3] = (
        "https://api.vk.com/method/some.apiMethodWithUnderscores?"
        f"access_token=token&v={vq.API.version}&"
        f"param1=1%2C2&foo=egg%2Cspam"
    )

    def test_token_owner_definer(self):
        api = vq.API("group_token", token_owner=vq.TokenOwner.GROUP)
        assert api.token_owner == vq.TokenOwner.GROUP

        api = vq.API("user_token", token_owner=vq.TokenOwner.USER)
        assert api.token_owner == vq.TokenOwner.USER

    @pytest.mark.parametrize(
        "token_owner,return_value",
        [(vq.TokenOwner.GROUP, {}), (vq.TokenOwner.USER, {"some": "user"})],
    )
    def test_auto_token_owner_definer(
        self, mocker: pytest_mock.MockerFixture, token_owner, return_value
    ):
        mocked_definer = mocker.patch.object(
            vq.API,
            "_make_sync_api_request",
            return_value=vq.AttrDict(return_value),
        )
        api = vq.API("token")
        mocked_definer.assert_called_once_with(
            "users.get", f"access_token={api.token}&v={api.version}"
        )
        assert api.token_owner == token_owner

    @pytest.mark.parametrize(
        "token,version,params,output",
        [
            (
                "token",
                "5.110",
                {"foo": "bar"},
                {"access_token": "token", "v": "5.110", "foo": "bar"},
            ),
            (
                "token",
                "5.110",
                {"access_token": "bar"},
                {"access_token": "bar", "v": "5.110"},
            ),
            (
                "token",
                "5.110",
                {"access_token": "bar", "v": "foo"},
                {"access_token": "bar", "v": "foo"},
            ),
            ("token", "5.110", {}, {"access_token": "token", "v": "5.110"},),
        ],
    )
    def test_fill_request_params(self, token, version, params, output):
        api = vq.API(
            token=token, version=version, token_owner=vq.TokenOwner.GROUP
        )
        assert api._fill_request_params(params) == output

    @pytest.mark.parametrize(
        "params,output",
        [
            ({"foo": "bar"}, {"foo": "bar"}),
            ({"foo": ["fizz", "bazz"]}, {"foo": "fizz,bazz"}),
            (
                {"list": [1, 2], "int": 1, "tuple": (1, 2), "set": {1, 2}},
                {"list": "1,2", "int": 1, "tuple": "1,2", "set": "1,2"},
            ),
        ],
    )
    def test_convert_collections_params(self, params, output):
        vq.API._convert_collections_params(params)
        assert params == output

    @pytest.mark.parametrize(
        "method_header,method_name,params,posted_message,return_value,output",
        async_data_request,
    )
    @pytest.mark.asyncio
    async def test_async_api_calls(
        self,
        mocker,
        method_header,
        method_name,
        params,
        posted_message,
        return_value,
        output,
    ):

        mocked_request_writer = mocker.patch.object(
            vq.RequestsSession, "write"
        )
        mocker.patch.object(
            vq.RequestsSession, "fetch_body", return_value=return_value
        )
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        getattr(api, method_header)
        getattr(api, method_name)
        response1 = await api(**params)
        response2 = await api.method(f"{method_header}.{method_name}", params)
        calls = [unittest.mock.call(posted_message)] * 2
        mocked_request_writer.assert_has_calls(calls)
        assert response1() == response2() == output

    @pytest.mark.parametrize(
        "method_header,method_name,params,posted_message,return_value,output",
        sync_data_request,
    )
    def test_sync_api_calls(
        self,
        mocker,
        method_header,
        method_name,
        params,
        posted_message,
        return_value,
        output,
    ):
        mocked_urlopen = mocker.patch(
            "urllib.request.urlopen",
            return_value=_ImplementedRead(return_value),
        )
        api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
        with api.synchronize():
            getattr(api, method_header)
            getattr(api, method_name)
            response1 = api(**params)
            response2 = api.method(f"{method_header}.{method_name}", params)
        calls = [
            unittest.mock.call(posted_message, context=unittest.mock.ANY)
        ] * 2
        mocked_urlopen.asser_has_calls(calls)
        assert response1() == response2() == output

    @pytest.mark.parametrize(
        "name,output",
        [
            ("some_fizz_bazz", "someFizzBazz"),
            ("some", "some"),
            ("some_mixedCase", "someMixedCase"),
        ],
    )
    def test_convert_name(self, name, output):
        assert vq.API._convert_name(name) == output

    def test_check_errors(self):
        vq.API._check_errors({"response": "normal response"})
        with pytest.raises(vq.VkApiError):
            vq.API._check_errors(
                {
                    "error": {
                        "error_msg": 1,
                        "error_code": 1,
                        "request_params": {},
                    }
                }
            )

    def test_autocomplete_params(self, mocker: pytest_mock.MockerFixture):
        api = vq.API(
            "token",
            token_owner=vq.TokenOwner.GROUP,
            autocomplete_params={"foo": "bar"},
        )
        mocked_rout = mocker.patch.object(vq.API, "_route_request_scheme")
        with api.synchronize():
            api.some.egg(...)
            api.some.egg(..., other="value")
            api.some.egg(..., foo="fizz")

        token_and_version = {"access_token": "token", "v": "5.133"}
        calls = [
            unittest.mock.call(
                method_name=unittest.mock.ANY,
                request_params={"foo": "bar", **token_and_version},
            ),
            unittest.mock.call(
                method_name=unittest.mock.ANY,
                request_params={
                    "foo": "bar",
                    "other": "value",
                    **token_and_version,
                },
            ),
            unittest.mock.call(
                method_name=unittest.mock.ANY,
                request_params={"foo": "fizz", **token_and_version},
            ),
        ]
        mocked_rout.assert_has_calls(calls)


def test_token_owner():
    assert vq.TokenOwner.GROUP == "group"
    assert vq.TokenOwner.USER == "user"
