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


class TestRequestSession:

    @pytest.mark.asyncio
    async def test_setup_connection(self, mocker: pytest_mock.MockerFixture):
        session = vq.RequestsSession("hostname")
        mocked_open_connection = mocker.patch(
            "asyncio.open_connection",
            return_value=("reader", "writer")
        )
        await session._setup_connection()
        mocked_open_connection.assert_called_once_with(
            "hostname", 443, ssl=unittest.mock.ANY
        )
        assert session.writer == "writer"
        assert session.reader == "reader"

    @pytest.mark.asyncio
    async def test_write(self, mocker: pytest_mock.MockerFixture):
        session = vq.RequestsSession("hostname")
        session.writer = _StreamWriter()
        mocked_drain = mocker.patch.object(session.writer, "drain")
        mocked_write = mocker.patch.object(session.writer, "write")
        mocked_setup = mocker.patch.object(session, "_setup_connection")

        # Without ConnectionResetError
        await session.write(b"foo")
        mocked_drain.assert_called_once()
        mocked_write.assert_called_once_with(b"foo")

        mocked_drain.reset_mock()
        mocked_write.reset_mock()

        # With ConnectionResetError
        mocked_drain.side_effect = ConnectionResetError()
        await session.write(b"foo")
        mocked_setup.assert_called_once()
        mocked_write.assert_called_once_with(b"foo")

    @pytest.mark.asyncio
    async def test_write_reset_connection(self, mocker: pytest_mock.MockerFixture):
        def setup_connection(*args, **kwars):
            breakpoint()
            self.writer = _StreamWriter()

        session = vq.RequestsSession("hostname")
        mocked_setup = mocker.patch.object(
            session, "_setup_connection", side_effect=lambda self: True, autospec=vq.RequestsSession._setup_connection)
        await session.write(b"foo")
        mocked_setup.assert_called_once()
        await session.write(b"foo")
        mocked_setup.assert_called_once()








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
