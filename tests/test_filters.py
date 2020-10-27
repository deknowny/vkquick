"""
Test filters
"""
import vkquick as vq
import pytest


class TestBaseFilter:
    def test_call(self):
        event_handler = vq.EventHandler()
        filter_object1 = object()
        filter_object2 = object()
        vq.Filter.__call__(filter_object1, event_handler)
        vq.Filter.__call__(filter_object2, event_handler)
        assert event_handler.filters == [filter_object1, filter_object2]

    def test_invalid_call(self):
        with pytest.raises(TypeError):
            vq.Filter.__call__(..., ...)


class TestEnable:
    def test_init(self):
        inst = vq.Enable()
        assert inst.enabled
        inst = vq.Enable(False)
        assert not inst.enabled

    def test_passed_decision(self):
        inst_enabled = vq.Enable()
        event = vq.Event({})
        decision = inst_enabled.make_decision(event)
        assert decision == (True, inst_enabled.passed_decision)

    def test_not_passed_decision(self):
        inst_disable = vq.Enable(False)
        event = vq.Event({})
        decision = inst_disable.make_decision(event)
        assert decision == (False, inst_disable.not_passed_decision)
