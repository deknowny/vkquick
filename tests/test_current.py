import vkquick as vq
import pytest


class SomeClassThatHasAPI:
    api = vq.current.fetch("api_spec", "api")


def test_fetch():
    vq.current.objects.api = 1
    inst1 = SomeClassThatHasAPI()
    vq.current.objects.api_spec = 1
    inst2 = SomeClassThatHasAPI()
    assert inst1.api == inst2.api == 1
    del vq.current.objects()["api_spec"]
    del vq.current.objects()["api"]
    with pytest.raises(NameError):
        SomeClassThatHasAPI().api  # noqa
