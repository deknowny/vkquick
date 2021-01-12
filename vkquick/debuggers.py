"""
Реализация дебаггеров

Дебаггер -- терминальный визуализатор команд,
наглядно показывающий, что произошло во время
обработки события: подходит ли его тип, каково
решение фильтров самого обработчика, какие
аргументы были переданы в реакцию, и была ли реакция вызвана
вообще
"""
import functools
import os
import typing as ty

import huepy

from vkquick.base.debugger import Debugger
from vkquick.base.handling_status import HandlingStatus
from vkquick.wrappers.user import User

Color = ty.Callable[[str], str]
"""
Тайпинг обертки для подсветки текста
"""


true_grey = functools.partial(huepy.grey, key=90)
"""
Настоящий серый цвет
"""


def uncolored_text(text: str) -> str:
    """
    Текст оригинального цвета
    """
    return text


def uncolored_bad(string: str):
    return f"[-] {string}"


class ColoredDebugger(Debugger):
    """
    Цветной дебаггер
    """

    event_handler_passed_color: Color = staticmethod(huepy.green)
    event_handler_not_passed_color: Color = staticmethod(huepy.red)
    event_handler_taken_time_color: Color = staticmethod(true_grey)
    unpassed_filter_name_color: Color = staticmethod(huepy.yellow)
    passed_filter_name_color: Color = staticmethod(huepy.green)
    filter_decision_color: Color = staticmethod(uncolored_text)
    passed_argument_color: Color = staticmethod(huepy.cyan)
    separator_color: Color = staticmethod(true_grey)
    exception_header_color: Color = staticmethod(huepy.bad)
    exception_header_reaction_name_color: Color = staticmethod(huepy.red)
    event_header_separator_color: Color = staticmethod(true_grey)
    reactions_separator_color: Color = staticmethod(true_grey)
    exception_separator_color: Color = staticmethod(true_grey)
    sender_name_color: Color = staticmethod(huepy.green)
    sender_command_color: Color = staticmethod(huepy.cyan)

    exception_header_template_wrapper = staticmethod(huepy.bad)

    sender_info_template: str = "Новое сообщение от `{sender_name}` с текстом `{sender_command}`"
    event_header_template: str = "{sender_info}\n{separator}\n\n"
    event_header_separator_symbol: str = "="
    reactions_separator_symbol: str = "-"
    exception_separator_symbol: str = "!"
    handlers_separator: str = "\n{separator}\n"
    exceptions_template: str = "\n{separator}\n{exceptions}"
    exception_header_template: str = "Реакция `{reaction_name}` при вызове выбросила исключение:\n\n"
    event_handler_header_template: str = "[{reaction_name}] {taken_time}\n"
    event_handler_argument_taken_time_template: str = "({taken_time}s)"
    event_handler_header_taken_time_digits_format_spec: str = ".6f"
    event_handler_filters_decision_separator: str = "\n"
    filter_info_template: str = "-> {filter_name}: {decision_description}"
    event_handler_arguments_separator: str = ""
    event_handler_arguments_template: str = "\n{arguments}"
    event_handler_argument_template: str = "    >> {name}: {value!s}\n"

    # Да, я устал.

    def render(self):
        """
        Основной метод визуализации, выстраивающий
        сообщение для отображения в терминале
        """
        header = self.build_header()
        body = self.build_body()
        exception = self.build_exception()
        result_message = header + body + exception
        return result_message

    def build_header(self) -> str:
        """
        Выстраивает хедер сообщения: тип события и время,
        когда завершилась его обработка
        """
        sender_info = self.sender_info_template.format(
            sender_name=self.sender_name_color(self._sender_name),
            sender_command=self.sender_command_color(self._message_text),
        )
        header = self.event_header_template.format(
            sender_info=sender_info,
            separator=self.build_separator(
                self.event_header_separator_symbol,
                self.event_header_separator_color,
            ),
        )
        return header

    def build_body(self) -> str:
        """
        Выстраивает тело сообщения: разделенная /внезапно/
        разделителями информация о каждом обработчике
        """
        handling_messages: ty.List[str] = []
        for scheme in self._schemes:
            handling_message = self.build_event_handler_message(scheme)
            if scheme.all_filters_passed:
                handling_messages.insert(0, handling_message)
            else:
                handling_messages.append(handling_message)

        separator = self.build_separator(
            self.reactions_separator_symbol, self.reactions_separator_color
        )
        separator = self.handlers_separator.format(separator=separator)
        body_message = separator.join(handling_messages)
        return body_message

    def build_exception(self) -> str:
        """
        Выстраивает текст поднятых исключений
        """
        exceptions: ty.List[str] = []
        for scheme in self._schemes:
            if scheme.exception_text:
                exc_header = self.build_exception_header(scheme)
                exc_text = exc_header + scheme.exception_text
                exceptions.append(exc_text)

        exceptions: str = self.exception_separator_symbol.join(exceptions)
        if exceptions:
            separator = self.build_separator(
                self.exception_separator_symbol,
                self.exception_separator_color,
            )
            exceptions: str = self.exceptions_template.format(
                separator=separator, exceptions=exceptions
            )
        return exceptions

    def build_exception_header(
        self, scheme: HandlingStatus,
    ):
        """
        Выстраивает заголовок для исключения
        """
        reaction_name = scheme.reaction_name
        reaction_name = self.exception_header_reaction_name_color(
            reaction_name
        )
        text = self.exception_header_template.format(
            reaction_name=reaction_name
        )
        text = self.exception_header_template_wrapper(text)
        return text

    def build_event_handler_message(self, scheme: HandlingStatus,) -> str:
        """
        Собирает сообщение о конкретном обработчике.
        В начале находится его имя, далее следует
        информация о каждом из фильтров: имя и описание его решения.
        Если реакция была вызвана с аргументами -- они также
        будут отображены
        """
        header = self.build_event_handler_header(scheme)
        filters_decision = self.build_event_handler_filters_decision(scheme)
        arguments = self.build_event_handler_arguments(scheme)

        return header + filters_decision + arguments

    def build_event_handler_header(self, scheme: HandlingStatus,) -> str:
        """
        Собирает заголовок обработчика для сообщения
        """
        if scheme.all_filters_passed:
            header_color = self.event_handler_passed_color
        else:
            header_color = self.event_handler_not_passed_color
        reaction_name = scheme.reaction_name
        reaction_name = header_color(reaction_name)
        taken_time = scheme.taken_time
        taken_time = format(
            taken_time,
            self.event_handler_header_taken_time_digits_format_spec,
        )
        taken_time = self.event_handler_argument_taken_time_template.format(
            taken_time=taken_time
        )
        taken_time = self.event_handler_taken_time_color(taken_time)
        header = self.event_handler_header_template.format(
            reaction_name=reaction_name, taken_time=taken_time
        )
        return header

    def build_event_handler_filters_decision(
        self, scheme: HandlingStatus,
    ) -> str:
        """
        Собирает решение фильтров для сообщения
        """
        filters_gen = self._generate_filters_message(scheme)
        filters_decision: ty.List[str] = list(filters_gen)
        filters_decision: str = self.event_handler_filters_decision_separator.join(
            filters_decision
        )
        return filters_decision

    def build_event_handler_arguments(self, scheme: HandlingStatus,) -> str:
        """
        Собирает аргументы для сообщения
        """
        arguments_gen = self._generate_arguments_message(scheme)
        arguments: ty.List[str] = list(arguments_gen)
        arguments: str = self.event_handler_arguments_separator.join(
            arguments
        )
        arguments: str = self.event_handler_arguments_template.format(
            arguments=arguments
        )
        return arguments

    def _generate_filters_message(
        self, scheme: HandlingStatus,
    ) -> ty.Generator[str, None, None]:
        """
        Генерирует информацию по каждому фильтру обработчика
        """
        for filter_response in scheme.filters_response:
            filter_name, decision = filter_response
            decision_description = self.filter_decision_color(
                decision.description
            )
            if decision.passed:
                filter_name = self.passed_filter_name_color(filter_name)
            else:
                filter_name = self.unpassed_filter_name_color(filter_name)
            filter_info = self.filter_info_template.format(
                filter_name=filter_name,
                decision_description=decision_description,
            )
            yield filter_info

    def _generate_arguments_message(
        self, scheme: HandlingStatus,
    ) -> ty.Generator[str, None, None]:
        """
        Генерирует информацию по каждому аргументу, переданного
        в реакцию
        """
        for name, value in scheme.passed_arguments.items():
            name = self.passed_argument_color(name)
            argument_info = self.event_handler_argument_template.format(
                name=name, value=value
            )
            yield argument_info

    @staticmethod
    def build_separator(
        sep_symbol: str, color: Color = uncolored_text
    ) -> str:
        """
        Выстраивает сепаратор, основываясь
        на длине терминального окна
        """
        size = os.get_terminal_size().columns
        separator = sep_symbol * size
        separator = color(separator)
        return separator


class UncoloredDebugger(ColoredDebugger):
    """
    Дебаггер без цвета
    """

    event_handler_passed_color: Color = staticmethod(uncolored_text)
    event_handler_not_passed_color: Color = staticmethod(uncolored_text)
    event_handler_taken_time_color: Color = staticmethod(uncolored_text)
    passed_filter_name_color: Color = staticmethod(uncolored_text)
    unpassed_filter_name_color: Color = staticmethod(uncolored_text)
    filter_decision_color: Color = staticmethod(uncolored_text)
    passed_argument_color: Color = staticmethod(uncolored_text)
    separator_color: Color = staticmethod(uncolored_text)
    exception_header_color: Color = staticmethod(uncolored_text)
    exception_header_reaction_name_color: Color = staticmethod(uncolored_text)
    event_header_separator_color: Color = staticmethod(uncolored_text)
    reactions_separator_color: Color = staticmethod(uncolored_text)
    exception_separator_color: Color = staticmethod(uncolored_text)
    sender_name_color: Color = staticmethod(uncolored_text)
    sender_command_color: Color = staticmethod(uncolored_text)

    exception_header_template_wrapper = staticmethod(uncolored_bad)
