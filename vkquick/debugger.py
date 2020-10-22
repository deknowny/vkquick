"""
Реализация дебаггера
"""
import dataclasses
import datetime
import os
import typing as ty

import huepy

import vkquick.event_handling.handling_info_scheme
import vkquick.events_generators


@dataclasses.dataclass
class Debugger:
    """
    Дебаггер -- терминальный визуализатор команд,
    наглядно показывающий, что произошло во время
    обработки события: подходит ли его тип, каково
    решение фильтров самого обработчика, какие
    аргументы были переданы в реакцию и была ли реакция вызвана
    вообще
    """

    event: vkquick.events_generators.event.Event
    """
    Событие, которое было обработано
    """
    schemes: ty.List[
        vkquick.event_handling.handling_info_scheme.HandlingInfoScheme
    ]
    """
    Набор отчетов об обработке, сформированных обработчиками/командами
    """

    def render(self):
        """
        Основной метод визуализации, выстраивающий
        сообщение для отображения в терминале
        """
        header = self._build_header()
        body = self._build_body()
        result_message = header + body
        return result_message

    def _build_header(self) -> str:
        """
        Выстраивает хедер сообщения: тип события и время,
        когда завершилась его обработка
        """
        summary_taken_time = 0
        for scheme in self.schemes:
            summary_taken_time += scheme["taken_time"]
        summary_taken_time_header = f"({summary_taken_time:.6f}s)"
        summary_taken_time_header = huepy.grey(
            summary_taken_time_header, key=90
        )
        event_header = f"-> {self.event.type} {summary_taken_time_header}\n"
        separator = self._build_separator("=")
        event_header += f"{separator}\n\n"
        return event_header

    def _build_body(self) -> str:
        """
        Выстраивает тело сообщения: разделенная /внезапно/
        разделителями информация о каждом обработчике
        """
        handling_messages: ty.List[str] = []
        for scheme in self.schemes:
            if scheme["is_correct_event_type"]:
                handling_message = self._build_event_handler_message(scheme)
                if scheme["are_filters_passed"]:
                    handling_messages.insert(0, handling_message)
                else:
                    handling_messages.append(handling_message)

        separator = self._build_separator("-")
        separator = f"\n{separator}\n\n"
        body_message = separator.join(handling_messages)
        return body_message

    def _build_event_handler_message(
        self,
        scheme: vkquick.event_handling.handling_info_scheme.HandlingInfoScheme,
    ) -> str:
        """
        Собирает сообщение о конкретном обработчике.
        В начале находится его имя, далее следует
        информация о каждом из фильтров: имя и описание его решения.
        Если реакция была вызвана с аргументами -- они также
        будут отображены
        """
        if scheme["are_filters_passed"]:
            header_color = huepy.green
        else:
            header_color = huepy.red
        handler_name = scheme["handler"].reaction.__name__
        handler_name = header_color(handler_name)
        taken_time = scheme["taken_time"]
        taken_time = f"({taken_time:.6f}s)"
        taken_time = huepy.grey(taken_time, key=90)
        header = f"[{handler_name}] {taken_time}\n"

        filters_gen = self._generate_filters_message(scheme)
        filters_decisions: ty.List[str] = list(filters_gen)
        filters_decisions: str = "\n".join(filters_decisions)

        arguments_gen = self._generate_arguments_message(scheme)
        arguments: ty.List[str] = list(arguments_gen)
        arguments: str = "".join(arguments)

        return header + filters_decisions + arguments

    @staticmethod
    def _generate_filters_message(
        scheme: vkquick.event_handling.handling_info_scheme.HandlingInfoScheme,
    ) -> ty.Generator[str, None, None]:
        """
        Генерирует информацию по каждому фильтру обработчика
        """
        for decision in scheme["filters_decision"]:
            decision_description = decision[1]
            filter_name = decision[2]
            filter_name = huepy.yellow(filter_name)
            filter_info = f"{filter_name}: {decision_description}"
            yield filter_info

    @staticmethod
    def _generate_arguments_message(
        scheme: vkquick.event_handling.handling_info_scheme.HandlingInfoScheme,
    ) -> ty.Generator[str, None, None]:
        """
        Генерирует информацию по каждому аргументу, переданного
        в реакцию
        """
        for name, value in scheme["passed_arguments"].items():
            name = huepy.cyan(name)
            argument_info = f"\n    > {name}: {value!s}"
            yield argument_info

    @staticmethod
    def _build_separator(sep_symbol: str) -> str:
        """
        Выстраивает сепаратор, основываясь
        на длине терминального окна
        """
        size = os.get_terminal_size().columns
        separator = sep_symbol * size
        separator = huepy.grey(separator, key=90)
        return separator
