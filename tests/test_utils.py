import pytest
import vkquick as vq


@pytest.mark.parametrize(
    "chat_id,peer_id",
    [(123, 2_000_000_123), (4566, 2_000_004_566), (0, 2_000_000_000)],
)
def test_peer(chat_id, peer_id):
    assert vq.peer(chat_id) == peer_id
