import os
import unittest.mock

import pytest
import pytest_mock
import vkquick as vq


class _StreamWriter:
    def write(self, value):
        ...

    def close(self):
        ...

    async def drain(self):
        ...


class _StreamReader:
    def __init__(self, message: bytes):
        self.message = message

    async def readline(self):
        line = b""
        for letter in map(bytes, zip(self.message)):
            line += letter
            if letter == b"\n":
                break
        self.message = self.message[len(line) :]
        return line

    async def read(self, length: int):
        chunk = self.message[:length]
        self.message = self.message[length:]
        return chunk


@pytest.mark.parametrize(
    "chat_id,peer_id",
    [(123, 2_000_000_123), (4566, 2_000_004_566), (0, 2_000_000_000)],
)
def test_peer(chat_id, peer_id):
    assert vq.peer(chat_id) == peer_id


@pytest.mark.parametrize("side", [10, 20])
def test_random_id(side, mocker: pytest_mock.MockerFixture):
    mocked_random = mocker.patch("random.randint", return_value=...)
    call = vq.random_id()
    mocked_random.asssert_called_once_with(-side, +side)
    assert call is ...


@pytest.mark.parametrize("key", ["foo", "bar"])
def test_safe_dict(key):
    assert "{" + key + "}" == vq.SafeDict().__missing__(key)


class TestAttrDict:
    def test_recursive_getattr(self):
        data = vq.AttrDict({"a": {"b": {"c": 1}}})
        assert data.a.b.c == 1

    def test_lists(self):
        data = vq.AttrDict({"a": [[[], {"b": 1}]]})
        assert data.a[0][0]() == []
        assert data.a[0][1].b == 1

    def test_calling(self):
        data = vq.AttrDict({"a": {"b": 1}})
        assert data("a")() == {"b": 1} == data("a")()
        assert isinstance(data("a"), vq.AttrDict)

    def test_getitem(self):
        data = vq.AttrDict({"a": {"b": 1}})
        assert isinstance(data["a"], dict)

    def test_setattr(self):
        data = vq.AttrDict({})
        data.item = "foo"
        assert data.item == data["item"] == "foo"

    def test_setitem(self):
        data = vq.AttrDict({})
        data["item"] = "foo"
        assert data.item == data["item"] == "foo"

    @pytest.mark.parametrize(
        "value,output",
        [({"a": "b"}, "AttrDict({'a': 'b'})"), ({1: 2}, "AttrDict({1: 2})")],
    )
    def test_repr(self, value, output):
        assert repr(vq.AttrDict(value)) == output

    def test_bool(self):
        assert not (vq.AttrDict())
        assert vq.AttrDict({"a": 1})

    def test_contains(self):
        assert "a" in vq.AttrDict({"a": 1})
        assert "a" not in vq.AttrDict({"b": 1})

    def test_len(self):
        assert len(vq.AttrDict({"a": 1, "b": 2})) == 2
        assert len(vq.AttrDict()) == 0

    def test_eq(self):
        assert vq.AttrDict({"a": 1, "b": 2}) == {"a": 1, "b": 2}
        assert vq.AttrDict() == {}

def test_clear_console(mocker: pytest_mock.MockerFixture):
    mocked_system = mocker.patch("os.system")
    original_os_name = os.name
    os.name = "nt"
    vq.clear_console()
    os.name = "posix"
    vq.clear_console()
    calls = [
        unittest.mock.call("cls"),
        unittest.mock.call("clear"),
    ]
    mocked_system.assert_has_calls(calls)
    os.name = original_os_name
