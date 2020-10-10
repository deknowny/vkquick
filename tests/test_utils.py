import pytest
import vkquick as vq


@pytest.mark.parametrize(
    "chat_id,peer_id",
    [(123, 2_000_000_123), (4566, 2_000_004_566), (0, 2_000_000_000)],
)
def test_peer(chat_id, peer_id):
    assert vq.peer(chat_id) == peer_id


attrdict_data = [
    ({"a": 1}, )
]


class TestAttrDict:

    def test_recursive_getattr(self):
        data = vq.AttrDict({"a": {"b": {"c": 1}}})
        assert data.a.b.c == 1

    def test_lists(self):
        data = vq.AttrDict(
            {"a": [[[], {"b": 1}]]}
        )
        assert data.a[0][0] == []
        assert data.a[0][1].b == 1

    def test_calling(self):
        data = vq.AttrDict({"a": {"b": 1}})
        assert data("a").mapping_ == {"b": 1}
        assert isinstance(data("a"), vq.AttrDict)

    def test_getitem(self):
        data = vq.AttrDict({"a": {"b": 1}})
        assert isinstance(data["a"], dict)