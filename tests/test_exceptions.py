"""
Test `exceptions.py` module
"""
import pytest

import vkquick as vq


class TestVkApiError:

    error_responses = [
        {
            "error_code": 5,
            "error_msg": "User authorization failed: invalid access_token.",
            "request_params": [
                {"key": "oauth", "value": "1"},
                {"key": "v", "value": "5.123"},
                {"key": "method", "value": "users.get"},
            ],
        },
        {
            "error_code": 10,
            "error_msg": "Some description lorem ipsum",
            "request_params": [
                {"key": "abc", "value": "fizzbazz"},
                {"key": "foo", "value": "bar"},
            ],
            "redirect_url": "localhost",
        },
    ]

    @pytest.mark.parametrize("scheme", error_responses)
    def test_destruct_response(self, scheme):
        exception = vq.VKAPIError.destruct_response({"error": scheme.copy()})
        assert exception.status_code == scheme["error_code"]
        assert exception.request_params == {
            item["key"]: item["value"] for item in scheme["request_params"]
        }
        assert exception.description == scheme["error_msg"]
        del scheme["error_msg"]
        del scheme["request_params"]
        del scheme["error_code"]
        assert exception.extra_fileds == scheme

    def test_str(self):
        inst = vq.VKAPIError.destruct_response(
            {
                "error": {
                    "error_code": 5,
                    "error_msg": "User authorization failed: invalid access_token.",
                    "request_params": [
                        {"key": "oauth", "value": "1"},
                        {"key": "v", "value": "5.123"},
                        {"key": "method", "value": "users.get"},
                    ],
                }
            }
        )
        assert str(inst) == inst.pretty_exception_text
