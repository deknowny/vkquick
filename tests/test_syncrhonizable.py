import inspect

import vkquick as vq


class Example(vq.Synchronizable):
    @vq.synchronizable_function
    async def foo(self):
        ...

    @foo.sync_edition
    def foo(self):
        ...


def test_synchronizable_function():
    example = Example()
    assert inspect.iscoroutinefunction(example.foo)
    with example.synchronize():
        assert not inspect.iscoroutinefunction(example.foo)
