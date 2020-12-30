"""
Test filters
"""
import vkquick as vq
import pytest


class TestBaseFilter:
    def test_call(self):
        command = vq.Command()
        filter_object1 = vq.Action("123")
        filter_object2 = vq.Enable()
        filter_object1(command)
        filter_object2(command)
        assert command.filters == [command, filter_object1, filter_object2]


# class TestEnable:
#     def test_init(self):
#         inst = vq.Enable()
#         assert inst.enabled
#         inst = vq.Enable(False)
#         assert not inst.enabled
#
#     def test_passed_decision(self):
#         inst_enabled = vq.Enable()
#         event = vq.Event({})
#         decision = inst_enabled.make_decision(event)
#         assert decision == (True, inst_enabled.passed_decision)
#
#     def test_not_passed_decision(self):
#         inst_disable = vq.Enable(False)
#         event = vq.Event({})
#         decision = inst_disable.make_decision(event)
#         assert decision == (False, inst_disable.not_passed_decision)
