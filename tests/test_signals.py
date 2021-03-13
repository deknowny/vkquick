import pytest
import pytest_mock
import vkquick as vq
import vkquick.resolvers.signal_handler


def test_create_signal_via_bot(make_bot, mocker: pytest_mock.MockerFixture):
    bot: vq.Bot = make_bot()

    def signal():
        ...

    signal = mocker.create_autospec(signal)
    signal.__name__ = "signal"
    signal = bot.add_signal_handler(signal)

    bot.call_signal("signal")

    signal.handler.assert_called_once()


def test_create_signal_via_exist_signal_handler(
    make_bot, mocker: pytest_mock.MockerFixture
):
    bot: vq.Bot = make_bot()

    def signal():
        ...

    signal = mocker.create_autospec(signal)
    signal.__name__ = "signal"
    signal = vkquick.resolvers.signal_handler.SignalHandler(signal)
    signal = bot.add_signal_handler(signal)

    bot.call_signal("signal")

    signal.handler.assert_called_once()


def test_signal_with_args(make_bot, mocker: pytest_mock.MockerFixture):
    bot: vq.Bot = make_bot()

    def signal(arg1, arg2):
        ...

    signal = mocker.create_autospec(signal)
    signal.__name__ = "signal"
    signal = bot.add_signal_handler(signal)

    bot.call_signal("signal", 1, arg2=2)

    signal.handler.assert_called_once_with(1, arg2=2)


def test_signal_extra_brackets(make_bot, mocker: pytest_mock.MockerFixture):

    bot: vq.Bot = make_bot()

    def signal():
        ...

    signal = mocker.create_autospec(signal)
    signal.__name__ = "signal"
    signal = vkquick.resolvers.signal_handler.SignalHandler()(signal)
    signal = bot.add_signal_handler(signal)

    bot.call_signal("signal")

    signal.handler.assert_called_once()


def test_signal_with_param_extra_names(
    make_bot, mocker: pytest_mock.MockerFixture
):

    bot: vq.Bot = make_bot()

    def signal():
        ...

    signal = mocker.create_autospec(signal)
    signal.__name__ = "signal"
    signal = vkquick.resolvers.signal_handler.SignalHandler(extra_names=["signal_extra_name"])(signal)
    signal = bot.add_signal_handler(signal)

    bot.call_signal("signal")
    bot.call_signal("signal_extra_name")

    assert signal.handler.call_count == 2


def test_signal_with_param_all_names(
    make_bot, mocker: pytest_mock.MockerFixture
):

    bot: vq.Bot = make_bot()

    def signal():
        ...

    signal = mocker.create_autospec(signal)
    signal.__name__ = "signal"
    signal = vkquick.resolvers.signal_handler.SignalHandler(all_names=["signal_real_name"])(signal)
    signal = bot.add_signal_handler(signal)

    bot.call_signal("signal")
    bot.call_signal("signal_real_name")

    signal.handler.assert_called_once()


def test_raises_signal():
    with pytest.raises(ValueError):
        vkquick.resolvers.signal_handler.SignalHandler(extra_names=["a"], all_names=["b"])
