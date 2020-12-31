import collections

import vkquick as vq
import pytest
import pytest_mock
import huepy

import unittest.mock


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
        assert vq.ColoredDebugger.build_separator("+") == "+"*10
    #
    # @pytest.mark.parametrize(
    #     "sizes,color,symbol",
    #     [((40, ...), huepy.red, "="), ((50, ...), huepy.green, "?")],
    # )
    # def test_build_separator(
    #     self, mocker: pytest_mock.MockerFixture, sizes, color, symbol
    # ):
    #     terminal_size = collections.namedtuple(
    #         "TerminalSize", ["columns", "lines"]
    #     )
    #     terminal_size = terminal_size(*sizes)
    #     mocked_get_terminal_size = mocker.patch(
    #         "os.get_terminal_size", return_value=terminal_size
    #     )
    #     vq.Debugger.separator_color = color
    #     separator = color(symbol * terminal_size.columns)
    #     debugger_separator = vq.Debugger.build_separator(symbol, color)
    #     mocked_get_terminal_size.assert_called()
    #     assert debugger_separator == separator
    #
    # # @pytest.mark.parametrize("template,event_type,separator", [
    # #     ("{event_type}{separator}", "type", "sep"),
    # #     ("", "foo", "bar")
    # # ])
    # # def test_build_header(self, mocker: pytest_mock.MockerFixture, template, event_type, separator):
    # #     debugger = vq.Debugger(vq.AttrDict({"type": event_type}), [])
    # #     result = debugger.build_header()
    # #     assert result == template.format(event_type=event_type, separator=separator)
