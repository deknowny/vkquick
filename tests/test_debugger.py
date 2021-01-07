import collections

import vkquick as vq
import pytest
import pytest_mock
import huepy

import unittest.mock

debugger_template = """
Новое сообщение от `Tom` с текстом `foo 123`
==============================

[foo] (0.500000s)
-> Command: passed
    >> arg: 123

------------------------------
[bar] (0.100000s)
-> Command: not passed

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
[-] Реакция `foo` при вызове выбросила исключение:

Exception!
""".strip()


@pytest.mark.parametrize("input,output", [("123", "123"), ("abc", "abc")])
def test_uncolered_text(input, output):
    assert vq.uncolored_text(input) == output


class TestDebugger:
    def test_render(self, mocker: pytest_mock.MockerFixture):
        mocked_event = mocker.Mock()
        mocked_event.msg = {}
        debugger = vq.ColoredDebugger(None, mocked_event, [])
        mocked_build_header = mocker.patch.object(
            debugger, "build_header", return_value="hello"
        )
        mocked_build_body = mocker.patch.object(
            debugger, "build_body", return_value="world"
        )
        mocked_build_exception = mocker.patch.object(
            debugger, "build_exception", return_value="exception"
        )
        result = debugger.render()
        assert result == "helloworldexception"
        mocked_build_header.assert_called()
        mocked_build_body.assert_called()
        mocked_build_exception.assert_called()

    def test_build_separator(self, mocker: pytest_mock.MockerFixture):
        mocked_terminal_size = mocker.patch("os.get_terminal_size")
        mocked_terminal_size.return_value = mocked_terminal_size
        mocked_terminal_size.columns = 10
        assert vq.ColoredDebugger.build_separator("+") == "+" * 10

    def test_result(self, mocker):
        size = mocker.patch("os.get_terminal_size")
        size.return_value = size
        size.columns = 30
        debugger = vq.UncoloredDebugger(
            sender_name="Tom",
            message_text="foo 123",
            schemes=[
                vq.HandlingStatus(
                    reaction_name="foo",
                    all_filters_passed=True,
                    taken_time=0.5,
                    filters_response=[
                        ("Command", vq.Decision(True, "passed"))
                    ],
                    passed_arguments={"arg": 123},
                    exception_text="Exception!",
                ),
                vq.HandlingStatus(
                    reaction_name="bar",
                    all_filters_passed=False,
                    taken_time=0.1,
                    filters_response=[
                        ("Command", vq.Decision(False, "not passed"))
                    ],
                ),
            ],
        )
        assert debugger.render().strip() == debugger_template
