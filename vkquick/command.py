from __future__ import annotations

import asyncio
import functools
import re
import time
import inspect
import concurrent.futures
import typing as ty

from vkquick.utils import AttrDict, sync_async_run, sync_async_callable
from vkquick.context import Context
from vkquick.base.handling_status import HandlingStatus
from vkquick.base.filter import Filter, Decision
from vkquick.events_generators.event import Event
from vkquick.base.text_cutter import TextCutter, UnmatchedArgument
from vkquick.shared_box import SharedBox
from vkquick.text_cutters.regex import Regex


# TODO: payload
class Command(Filter):
    """
    Команда -- продвинутая реакция на новое сообщение,
    совмещающая в себе возможности указания удобной текстовой
    сигнатуры (имена, префиксы, аргументы...) и некоторых дополнительных
    фичах, о которых речь ниже. В 99% случаев вам не потребуется
    использовать ни один метод или поле, образованные инстансом команды,
    потому что они созданы для сторонних расширений,
    которые можно будет в бота подключить.
    Самое важное здесь просто познакомиться с аргументами,
    которые можно передать в инициализацию. Создавать команды просто,
    нужно лишь повесить декоратор над обработчиком команды (функцией, которую
    в последующем мы будем называть реакцией)

    Все созданные команды необходимо передать в инстанс бота либо через
    марки, либо при инициализации (см. пример примитивного бота в файле `vkquick/bot.py`)


    * `prefixes`:
        Префиксы, на которые реагирует команда

    * `names`:
        Имена, на которые реагирует команда.
        Фактически, это то, что идет сразу после префикса, т.е.

            @Command(prefixes=["/", "!"], names="hi")

        означает, что команда среагирует на:
            * !hi
            * /hi

    * `title`:
        Заголовок (название?) команды. В 2-3х словах, что делает команда.
        Исключение пользователя, генерация случайного числа... Используется
        так же в автодоке. По умолчанию команда называется так же, как и реакция

    * `description`:
        Полное описание того, что делает команда. Если у реакции есть
        докстринга, она будет использована в качестве описания

    * `routing_command_re_flags`:
        Этап парсинга команды можно разбить надвое:

            1. Проверка на совпадение префикса и имени с помощью регулярок
            2. Если прошел первый, идет валидация аргументов

        Так вот сюда можно передать флаги, которые будут использоваться
        в проверке первого этапа. По умолчанию это `re.IGNORECASE`,
        т.е. все команды не чувствительны к регистру символов.

        Pro tip: Если нужно передать несколько флагов, сделать можно так:

            ...
            routing_command_re_flags=re.IGNORECASE | re.DOTALL,
            ...

    * `on_invalid_argument`:
        Если вдруг человек передал некорректный по значению
        аргумент, то команда автоматически сообщит об этом,
        но вы можете установить собственное поведение, передав
        в качестве ключа аргумент, на который нужно реагировать, и
        функцию, в качестве значения, которая должна сработать.
        Функция принимает контекст

    * `on_invalid_filter`:
        Можно задать свое поведение фильтру, который не прошел,
        указав в ключе фильтр, а в значении саму функцию.
        Функция принимает в аргумент контекст

    * `extra`:
         Поля, которые можно передать для сторонних расширений.

    * `run_in_thread` & `run_in_process`:
        Команда может автоматически запустить реакцию
        в потоке/процессе (соответствуя названиям). Нельзя
        использовать одновременно и то, и другое, или же
        делать реакцию асинхронной (она и так асинхронно запустится)


    ## О реакциях
    Реакции -- обработчики самой команды, если она было вызвана.
    У реакций есть некоторые возможности и некоторые правила,
    с которыми их необходимо использовать.

    ### Как их делать
    Пример в самом начале файла
    (ха, ты реально думал, что я буду как попугай 200 раз показывать один и тот же код?)


    ### Быстрые ответы
    Давайте рассмотрим обычную команду, отвечающую `hello!` на `hi`
    (да, ты оказался прав(а) :P)

        import vkquick as vq


        @vq.Command(names=["hi"])
        def hello():
            return "hello!"

    Мы можем просто вернуть строку, и она отправится
    в ответ на сообщение пользователя! Если нужны расширенные
    возможности отправки сообщений, то для таких целей
    существует контекст (о нем речь ниже)

    ### Аргументы команды
    По умолчанию реакция не принимает ничего,
    а может принимать текстовые аргументы. Например,
    пользователю нужно передать какое-то значение (
    упоминание другого пользователя, или даже просто число).
    Конечно, можно измучить текст команды разными сплитами и
    потом с ужасом смотреть на получившийся плов. Этот класс
    дает возможности легкого добавления команд. Пусть команда `hello`,
    пример которой был выше, должна принимать какое-то слово -- то,
    как она должна называть нас, когда отвечает `hello!`. Например,
    му пишем `hi Tom`, и нам отвечают `Hello, Tom!`. Внимание на экран:

        import vkquick as vq


        @vq.Command(names=["hi"])
        def hello(name: vq.Word):
            return f"hello!, {name}"


    Теперь наша команда принимает аргумент в виде слова (т.е. имени).

    Можно указать несколько аргументов, которые должны принимать команда,
    просто перечислив их в аргументах самой реакции.

    Возможности типов для реакций на этом не заканчиваются. Например, можно
    указать максимальную длину слова (в нашем случае имени).

        import vkquick as vq


        @vq.Command(names=["hi"])
        def hello(name: vq.Word(max_length=10)):
            return f"hello!, {name}"

    Бот сам сообщит пользователю, если он передаст слово, длиной более
    чем в 10 символов.

    Если ваш линтер сходит с ума,
    тип аргумента можно передать через дефолтное значение
    (`str` в примере ниже опционален. Можно без него)

        import vkquick as vq


        @vq.Command(names=["hi"])
        def hello(name: str = vq.Word(max_length=10)):
            return f"hello!, {name}"

    Обобщая, вот всевозможные применения текстовых аргументов
    на примере `Integer`

        def foo(arg: int = vq.Integer()): ...
        def foo(arg: vq.Integer()): ...

        # Учитывайте, что некоторые аргументы все же требуют обязательных значений,
        # Например, `List`
        def foo(arg: int = vq.Integer): ...
        def foo(arg=vq.Integer): ...


    ### Контекст
    От вк во время нового сообщения прилетает много разной информации.
    Его можно получить, указав __первым__ аргументом функции тип контекста

        import vkquick as vq


        @vq.Command(names=["hi"])
        async def hello(ctx: vq.Context):
            \"""
            Здоровается с пользователем, передавая его имя
            \"""
            sender = await ctx.fetch_sender()
            return "Hi, {sender:<fn> <ln>}!"

    Если кратко о возможностях -- хранит сам объект события
    и содержит некоторые плюшки для быстрого взаимодействия.
    О всем о том можно почитать непосредственно его докстрингу (`context.py`)
    """

    def __init__(
        self,
        *,
        prefixes: ty.Iterable[str] = (),
        names: ty.Iterable[str] = (),
        title: ty.Optional[str] = None,
        argline: ty.Optional[str] = None,
        description: ty.Optional[str] = None,
        routing_command_re_flags: re.RegexFlag = re.IGNORECASE,
        on_invalid_argument: ty.Optional[
            ty.Dict[
                str,
                ty.Union[
                    sync_async_callable([Context], ...),
                    str,
                    sync_async_callable([], ...),
                ],
            ]
        ] = None,
        on_invalid_filter: ty.Optional[
            ty.Dict[
                ty.Type[Filter],
                ty.Union[
                    sync_async_callable([Context], ...),
                    str,
                    sync_async_callable([], ...),
                ],
            ]
        ] = None,
        human_style_arguments_name: ty.Optional[ty.Dict[str, str]] = None,
        extra: ty.Optional[dict] = None,
        run_in_thread: bool = False,
        run_in_process: bool = False,
        use_regex_escape: bool = True,
        any_text: bool = False,
        payload_names: ty.Collection[str] = ()
    ) -> None:
        self._description = description
        self._argline = argline
        self._names = None
        self._prefixes = None
        self._routing_command_re_flags = routing_command_re_flags
        self._extra = AttrDict(extra or {})
        self._description = description
        self._title = title
        self._human_style_arguments_name = human_style_arguments_name
        self._use_regex_escape = use_regex_escape
        self._payload_names = tuple(payload_names)

        self._filters: ty.List[Filter] = [self]
        self._reaction_arguments: ty.List[ty.Tuple[str, ty.Any]] = []
        self._reaction_context_argument_name = None

        self._invalid_filter_handlers = on_invalid_filter or {}
        self._invalid_argument_handlers = on_invalid_argument or {}

        if any_text and (prefixes or names):
            raise ValueError("Can't use `any_text` with `prefixes` or `names`")

        self._any_text = any_text

        if run_in_process and run_in_thread:
            raise ValueError(
                "Command can be run only in "
                "a process or in a thread, "
                "not both at the same time"
            )

        if run_in_thread:
            self._pool = concurrent.futures.ThreadPoolExecutor()
        elif run_in_process:
            self._pool = concurrent.futures.ProcessPoolExecutor()
        else:
            self._pool = None

        # Note: используется property
        self.prefixes = prefixes
        self.names = names
        self._build_routing_regex()

    @property
    def reaction_context_argument_name(self) -> ty.Optional[str]:
        return self._reaction_context_argument_name

    @property
    def payload_names(self) -> ty.Tuple[str, ...]:
        return self._payload_names

    @property
    def any_text(self) -> bool:
        return self._any_text

    @property
    def reaction_arguments(self) -> ty.List[ty.Tuple[str, ty.Any]]:
        """
        Текстовые аргументы, принимаемые командой
        """
        return self._reaction_arguments

    @property
    def title(self) -> ty.Optional[str]:
        """
        Имя команды (максимально краткое описание того, что она делает)
        """
        return self._title

    @property
    def description(self) -> str:
        """
        Описание команды. В случае отсутствия
        возвращает соответствующую строку об отсутствии описания
        """
        if self._description is None:
            return "Описание отсутствует"
        return self._description

    @property
    def extra(self) -> AttrDict:
        """
        Дополнительные параметры. Используется
        расширениями/плагинами для дополнительных возможностей
        """
        return self._extra

    @property
    def prefixes(self) -> ty.Tuple[str]:
        """
        Префиксы, на которые реагирует команда
        """
        return self._prefixes  # noqa

    @prefixes.setter
    def prefixes(self, value: ty.Iterable[str]) -> None:
        should_rebuild = self._prefixes is not None
        if isinstance(value, str):
            self._prefixes = (value,)
        else:
            self._prefixes = tuple(value)
        if should_rebuild:
            self._build_routing_regex()

    @property
    def names(self) -> ty.Tuple[str]:
        """
        Имена, на которые реагирует команда
        """
        return self._names  # noqa

    @names.setter
    def names(self, value: ty.Iterable[str]) -> None:
        should_rebuild = self._prefixes is not None
        if isinstance(value, str):
            self._names = (value,)
        else:
            self._names = tuple(value)
        if should_rebuild:
            self._build_routing_regex()

    @property
    def filters(self) -> ty.List[Filter]:
        """
        Фильтры, которые есть у команды (включая сам `Command`)
        """
        return self._filters

    @property
    def human_style_arguments_name(self) -> ty.Dict[str, str]:
        return self._human_style_arguments_name

    @property
    def invalid_argument_handlers(
        self,
    ) -> ty.Dict[str, ty.Union[sync_async_callable([Context], ...), str]]:
        """
        Обработчики, либо готовые ответы на некорректные аргументы
        """
        return self._invalid_argument_handlers

    @property
    def invalid_filter_handlers(
        self,
    ) -> ty.Dict[str, ty.Union[sync_async_callable([Context], ...), str]]:
        """
        Обработчики, либо готовые ответы на фильтры, которые не прошли
        """
        return self._invalid_filter_handlers

    @property
    def use_regex_escape(self):
        return self._use_regex_escape

    def __call__(self, reaction: sync_async_callable(..., ty.Optional[str])):
        self.reaction = reaction
        self._resolve_arguments()
        if self._argline is not None:
            self._spoof_args_from_argline()
        if self._description is None:
            self._description = inspect.getdoc(reaction)
        if self._title is None:
            self._title = reaction.__name__
        if not self._payload_names:
            self._payload_names = (reaction.__name__,)
        if self._pool is not None and inspect.iscoroutinefunction(reaction):
            raise ValueError(
                "Can't run a command in thread/process "
                "if it is a coroutine function"
            )
        return self

    async def handle_event(
        self, event: Event, shared_box: SharedBox
    ) -> HandlingStatus:
        start_handling_stamp = time.monotonic()
        context = Context(shared_box=shared_box, event=event,)
        (
            passed_every_filter,
            filters_decision,
        ) = await self.run_through_filters(context)
        if not passed_every_filter:
            end_handling_stamp = time.monotonic()
            taken_time = end_handling_stamp - start_handling_stamp
            return HandlingStatus(
                reaction_name=self.reaction.__name__,
                all_filters_passed=False,
                filters_response=filters_decision,
                taken_time=taken_time,
            )

        await self.call_reaction(context)

        end_handling_stamp = time.monotonic()
        taken_time = end_handling_stamp - start_handling_stamp
        return HandlingStatus(
            reaction_name=self.reaction.__name__,
            all_filters_passed=True,
            filters_response=filters_decision,
            passed_arguments=context.extra.reaction_arguments(),
            taken_time=taken_time,
        )

    async def run_through_filters(
        self, context: Context
    ) -> ty.Tuple[bool, ty.List[ty.Tuple[str, Decision]]]:
        """
        Проходит по всем обозначенным на команду фильтрам
        для выявления того, нужно ли ее вызывать на данное событие
        """
        decisions = []
        for filter_ in self.filters:
            decision = await sync_async_run(filter_.make_decision(context))
            decisions.append((filter_.__class__.__name__, decision))
            if not decision.passed:
                if filter_.__class__ in self._invalid_filter_handlers:
                    handler = self._invalid_filter_handlers[filter_.__class__]
                    await _optional_call_with_autoreply(handler, context)
                return False, decisions

        return True, decisions

    def on_invalid_filter(
        self, filter_: ty.Type[Filter], /
    ) -> ty.Callable[[sync_async_callable([Context], ...)], ...]:
        """
        Этим декоратором можно пометить обработчик, который будет
        вызван, если фильтр вернул ложь
        """

        def wrapper(handler):
            self._invalid_filter_handlers[filter_] = handler
            handler_parameters = inspect.signature(handler).parameters
            length_parameters = len(handler_parameters)
            if length_parameters not in (1, 0):
                raise KeyError(
                    f"Invalid argument handler should "
                    f"have one argument for context or nothing, "
                    f"got {length_parameters} arguments"
                )
            return handler

        return wrapper

    def on_invalid_argument(
        self,
        name: ty.Union[
            sync_async_callable([Context], ...),
            str,
            sync_async_callable([], ...),
        ],
    ) -> ty.Callable[[sync_async_callable([Context], ...)], ...]:
        """
        Этим декоратором можно пометить обработчик, который будет
        вызван, аргумент оказался некорректным по значению
        """

        def wrapper(handler):
            self._invalid_argument_handlers[name] = handler
            handler_parameters = inspect.signature(handler).parameters
            length_parameters = len(handler_parameters)
            if length_parameters not in (1, 0):
                raise KeyError(
                    f"Invalid argument handler should "
                    f"have one argument for context or nothing, "
                    f"got {length_parameters} arguments"
                )
            return handler

        if isinstance(name, str):
            return wrapper
        else:
            handler = name
            name = name.__name__
            real_handler = wrapper(handler)
            return real_handler

    async def make_decision(self, context: Context):
        if self.any_text:
            return Decision(True, "Команда полностью подходит")

        matched = self._command_routing_regex.match(context.msg.text)
        if matched:
            arguments_string = context.msg.text[matched.end() :]
        else:
            return Decision(
                False,
                f"Команда не подходит под шаблон `{self._command_routing_regex.pattern}`",
            )

        is_parsed, arguments = await self.init_text_arguments(
            arguments_string, context
        )

        if not is_parsed:
            if not arguments:
                return Decision(
                    False,
                    "Команде были переданы аргументы, которые не обозначены",
                )

            unparsed_argument_name, _ = arguments.popitem()

            return Decision(
                False,
                f"Не удалось выявить значение для аргумента `{unparsed_argument_name}`",
            )
        if self._reaction_context_argument_name is not None:
            arguments[self._reaction_context_argument_name] = context
        context.extra.reaction_arguments = arguments
        return Decision(True, "Команда полностью подходит")

    async def init_text_arguments(
        self, arguments_string: str, context: Context
    ) -> ty.Tuple[bool, dict]:
        """
        Инициализация текстовых аргументов из сообщения.
        Это работает каким-то чудом, просто поверьте
        """
        arguments = {}
        new_arguments_string = arguments_string.lstrip()
        for name, cutter in self._reaction_arguments:
            parsed_value, new_arguments_string = cutter.cut_part(
                new_arguments_string
            )
            if not self._argline:
                new_arguments_string = new_arguments_string.lstrip()
            arguments[name] = parsed_value
            # Значение от парсера некорректное или
            # Осталась часть, которую уже нечем парсить
            if (
                parsed_value is UnmatchedArgument
                or len(arguments) == len(self._reaction_arguments)
                and new_arguments_string
            ):
                if name in self._invalid_argument_handlers:
                    reaction = self._invalid_argument_handlers[name]
                    await _optional_call_with_autoreply(reaction, context)
                else:
                    for position, arg in enumerate(self._reaction_arguments):
                        if arg[0] == name:
                            await cutter.invalid_value(
                                position, not new_arguments_string, context,
                            )
                            break
                return False, arguments

        if "__argline_regex_part" in arguments:
            del arguments["__argline_regex_part"]

        if new_arguments_string:
            return False, arguments
        return True, arguments

    async def call_reaction(self, context: Context) -> None:
        """
        Вызывает реакцию, передавая все собранные аргументы.
        При вызове учитывается то, как реакцию запустить (поток/процесс...)
        и то, что она вернула. Если реакция вернула не `None`, это отправится
        в ответ на сообщение вызванной команды
        """
        if self._pool is not None:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                self._pool,
                functools.partial(
                    self.reaction, **context.extra["reaction_arguments"]
                ),
            )
        else:
            result = self.reaction(**context.extra["reaction_arguments"])
        result = await sync_async_run(result)
        if result is not None:
            await context.reply(message=result)

    def _spoof_args_from_argline(self):
        self._argline = self._argline.lstrip()
        argtype_regex = r"(\{[a-z][a-z0-9]+?\})"
        argline_parts = re.split(
            argtype_regex, self._argline, flags=re.IGNORECASE
        )
        spoofed_reaction_arguments = []
        real_reaction_arguments = dict(self._reaction_arguments)
        for part in argline_parts:
            if re.fullmatch(argtype_regex, part):
                arg_name = part[1:-1]
                if arg_name not in real_reaction_arguments:
                    raise KeyError(
                        f"Passed a linked argument `{arg_name}` in"
                        f"argline, but there isn't such"
                        f"in reaction signature"
                    )
                spoofed_reaction_arguments.append(
                    (arg_name, real_reaction_arguments[arg_name])
                )
            else:
                spoofed_reaction_arguments.append(
                    ("__argline_regex_part", Regex(part))
                )

        self._reaction_arguments = spoofed_reaction_arguments


    def _resolve_arguments(self) -> None:
        """
        Вызывается в момент декорирования для распознания того,
        какие аргументы следует передавать в реакцию
        """
        parameters = inspect.signature(self.reaction).parameters
        parameters = list(parameters.items())
        if not parameters:
            return
        seems_context, *cutters = parameters

        # def foo(ctx: Context): ...
        # def foo(ctx=Context)
        # def foo(ctx): ...
        if (
            seems_context[1].annotation is Context
            or seems_context[1].default is Context
            or (
                seems_context[1].annotation is seems_context[1].empty
                and seems_context[1].default is seems_context[1].empty
            )
        ):
            self._reaction_context_argument_name = seems_context[0]

        else:
            self._resolve_text_cutter(seems_context)

        for argument in cutters:
            self._resolve_text_cutter(argument)

    def _resolve_text_cutter(
        self, argument: ty.Tuple[str, inspect.Parameter]
    ):
        """
        Вызывается в момент декорирования.
        Определяет аргументы текстовой команды
        """
        # def foo(arg: int = vq.Integer()): ...
        # def foo(arg: vq.Integer()): ...
        # def foo(arg: int = vq.Integer): ...
        # def foo(arg=vq.Integer): ...
        name, value = argument
        if value.default != value.empty:
            cutter = value.default
        elif value.annotation != value.empty:
            cutter = value.annotation
        else:
            raise TypeError(
                f"The reaction argument `{name}` "
                f"should have a default value or an "
                f"annotation for specific text cutter, "
                f"nothing is now."
            )

        if inspect.isclass(cutter) and issubclass(cutter, TextCutter):
            real_type = cutter()
        elif isinstance(cutter, TextCutter):
            real_type = cutter
        else:
            if cutter is Context:
                raise TypeError(
                    "Context argument should be "
                    "the first in reactiom arguments"
                )
            raise TypeError(
                f"The reaction argument `{name}` should "
                "be `TextCutter` subclass or "
                f"instance, got `{value}`."
            )

        self._reaction_arguments.append((name, real_type))

    def _build_routing_regex(self):
        """
        Выстраивает регулярное выражение, по которому
        определяется вызов команды. Не включает в себя
        аргументы, т.к. для них задается своя логика фильтром
        """
        # Экранирование специальных символов, если такое указано
        if self.use_regex_escape:
            prefixes = map(re.escape, self.prefixes)
            names = map(re.escape, self.names)
        else:
            prefixes = self.prefixes
            names = self.names

        # Объединение имен и префиксов через или
        self._prefixes_regex = "|".join(prefixes)
        self._names_regex = "|".join(names)

        # Проверка длины, чтобы не создавать лишние группы
        if len(self.prefixes) > 1:
            self._prefixes_regex = f"(?:{self._prefixes_regex})"
        if len(self.names) > 1:
            self._names_regex = f"(?:{self._names_regex})"

        self._command_routing_regex = re.compile(
            self._prefixes_regex + self._names_regex,
            flags=self._routing_command_re_flags,
        )

    def __str__(self):
        return f"<Command title={self.title}, prefixes={self.prefixes}, names={self.names}>"


def _call_with_optional_context(func, context: Context):
    parameters = inspect.signature(func).parameters
    if len(parameters) == 1:
        return func(context)
    elif len(parameters) == 0:
        return func()
    else:
        raise TypeError("Handler to invalid can take from 0 to 1 parameters.")


async def _optional_call_with_autoreply(func, context: Context):
    if isinstance(func, str):
        response = func
    else:
        response = await sync_async_run(
            _call_with_optional_context(func, context)
        )
    if response is not None:
        await context.reply(response)
