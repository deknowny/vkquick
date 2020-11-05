"""
Сигналы — кастомные события. Например, вам нужно, чтобы
когда бот прекращал работу, происходила какая-то логика. Или
же у вас есть у вас есть вспомогательная функция для обращения
в базу данных. Для обоих случаев вы можете сделать обработчик сигнала.
Сигналы делятся на встроенные
(т.е. зарезервированные. `STARTUP`, `SHUTDOWN`... Всех их можно найти ниже)
и кастомные, которые можно использовать внутри своего бота (или даже внутри другого)

    import vkquick as vq


    # Создаст обработчик сигнала на событие по завершению работы бота
    @vq.SignalHandler(vq.ReservedSignal.SHUTDOWN)
    def shutdown():
        print("Turn off the bot...")


    # Создаст обработчик на кастомное событие
    @vq.SignalHandler("send_data")
    def send_data(data):
        print("Send the data to database...")
        return "OK!"


    # С инстансом `vq.Bot` в любой точке кода:
    response = bot.call_signal.send_data({"foo": "bar"})
    print(response)  # OK!
    # Не забудьте передать сам объект обработчика в бота
"""
from __future__ import annotations
import dataclasses
import enum
import typing as ty

import vkquick.utils


class ReservedSignal(enum.Enum):
    """
    Зарезервированные сигналы

    * `STARTUP`: Вызывается в момент запуска бота
    * `SHUTDOWN`: Вызывается в момент завершения работы бота
    * `POST_EVENT_HANDLING`: Вызывается после того, как все обработчики событий обработали событие.
    Передает первым аргументом само событие, а вторым -- список из `HandlingInfo`
    """

    STARTUP = enum.auto()
    SHUTDOWN = enum.auto()
    POST_EVENT_HANDLING = enum.auto()


SignalName = ty.Union[str, ReservedSignal]
"""
Тайпинг для имени сигнала. В принципе, в качестве имени можно использовтаь что
угодно, но мы рекомендуем использовать строки и именовать сигналы в `snake_case`,
чтобы их можно было удонбо вызвать через `__getattr__`
"""


@dataclasses.dataclass
class SignalHandler:
    """
    Обработчик сигнала (и кастомного, и зарезервированного). Пример
    есть в описании модуля
    """

    name: SignalName
    """
    Имя обрабатываемого сигнала
    """

    def __call__(
        self, reaction: vkquick.utils.sync_async_callable(..., ty.Any)
    ) -> SignalHandler:
        """
        Декорирование для передачи реакции на сигнал
        """
        self.reaction = reaction
        return self


@dataclasses.dataclass
class SignalCaller:
    """
    Сама логика по вызову сигналов. Можно интегрировать куда угодно
    """

    handlers: ty.Collection[SignalHandler] = dataclasses.field(
        default_factory=tuple
    )
    """
    Обработчики сигналов
    """
    signal_name: ty.Optional[SignalName] = None
    """
    Имя сигнала, которое нужно обработать 
    """

    def __getattr__(self, signal_name: SignalName) -> SignalCaller:
        """
        Так можно указать имя обработчика сигнала, который нужно вызвать
        """
        self.signal_name = signal_name
        return self

    def __call__(self, *args, **kwargs) -> ty.Any:
        """
        Вызов сигнала с нужным именем. Если сигнала с таким
        именем нет, ничего не случится.
        """
        signal_name = self.signal_name
        self.signal_name = None
        for handler in self.handlers:
            if handler.name == signal_name:
                return vkquick.utils.sync_async_run(
                    handler.reaction(*args, **kwargs)
                )

    def via_name(
        self, name: ty.Optional[SignalName], /, *args, **kwargs
    ) -> ty.Any:
        """
        Позволяет вызвать сигнал явно передав его имя
        """
        self.signal_name = name
        return self(*args, **kwargs)


def signal_handler(reaction) -> SignalHandler:
    """
    Создает обработчик сигнала по его имени
    """
    return SignalHandler(reaction.__name__)(reaction)
