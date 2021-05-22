from __future__ import annotations

import asyncio
import dataclasses
import os
import pathlib
import shutil
import typing as ty

import jinja2
from loguru import logger

from vkquick.api import API, TokenOwner
from vkquick.base.event_factories import BaseEventFactory
from vkquick.chatbot.package import Package
from vkquick.chatbot.storages import NewEvent, NewMessage
from vkquick.logger import update_logging_level
from vkquick.longpoll import GroupLongPoll, UserLongPoll


@dataclasses.dataclass
class App(Package):

    packages: ty.List[Package] = dataclasses.field(default_factory=list)
    debug: bool = True
    # Autodoc preferences
    name: str = "VK Quick Бот"
    description: str = "Чат-бот для ВКонтакте, написанный на Python с использованием VK Quick"
    site_title: str = "Документация к чат-боту"

    def __post_init__(self):
        if self.debug:
            update_logging_level("DEBUG")

        self.packages.append(self)
        for package in self.packages:
            for command in package.commands:
                command.update_prefix(*self.prefixes)

    async def route_event(self, new_event_storage) -> None:
        routing_coroutines = [
            package.handle_event(new_event_storage)
            for package in self.packages
        ]
        await asyncio.gather(*routing_coroutines)

    async def route_message(self, message_storage: NewMessage):
        routing_coroutines = [
            package.handle_message(message_storage)
            for package in self.packages
        ]
        await asyncio.gather(*routing_coroutines)

    def add_package(self, package: Package) -> None:
        self.packages.append(package)

    def run(
        self,
        *tokens: str,
        build_autodoc: bool = True,
        docs_directory: str = "autodocs",
        docs_filename: str = "index.html"
    ) -> None:
        asyncio.run(
            self.coroutine_run(
                *tokens,
                build_autodoc=build_autodoc,
                docs_directory=docs_directory,
                docs_filename=docs_filename
            ),
            debug=self.debug,
        )

    async def coroutine_run(
        self,
        *tokens,
        build_autodoc: bool = True,
        docs_directory: str = "autodocs",
        docs_filename: str = "index.html"
    ) -> None:
        if build_autodoc:
            self.render_autodoc(
                directory=docs_directory, filename=docs_filename
            )

        logger.opt(colors=True).success(
            "Run app (<b>{count}</b> bot{postfix})",
            count=len(tokens),
            postfix="s" if len(tokens) > 1 else "",
        )
        bots_init_coroutines = [
            Bot.via_token(token, self) for token in tokens
        ]
        bots = await asyncio.gather(*bots_init_coroutines)
        await self._call_startup(*bots)
        run_coroutines = [bot.run_polling() for bot in bots]
        try:
            await asyncio.gather(*run_coroutines)
        finally:
            await self._call_shutdown(*bots)
            for bot in bots:
                await bot.close_sessions()

    async def _call_startup(self, *bots: Bot) -> None:
        startup_coroutines = []
        for pkg in self.packages:
            for startup_handler in pkg.startup_handlers:
                for bot in bots:
                    startup_coroutines.append(startup_handler(bot))

        await asyncio.gather(*startup_coroutines)

    async def _call_shutdown(self, *bots: Bot) -> None:
        shutdown_coroutines = []
        for pkg in self.packages:
            for shutdown_handler in pkg.shutdown_handlers:
                for bot in bots:
                    shutdown_coroutines.append(shutdown_handler(bot))

        await asyncio.gather(*shutdown_coroutines)

    def render_autodoc(
        self, directory: str = "autodocs", filename: str = "index.html"
    ):
        autodoc_dir = pathlib.Path(__file__).parent.parent / "autodoc"
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(autodoc_dir / "templates")
        )
        main_template = env.get_template("index.html")

        saved_path_dir = pathlib.Path(directory)

        # Remove old files
        if saved_path_dir.exists():
            shutil.rmtree(saved_path_dir)

        # Recreate dir
        saved_path_dir.mkdir()

        # Copy assets
        shutil.copytree(autodoc_dir / "assets", saved_path_dir / "assets")

        saving_path = saved_path_dir / filename
        with open(saving_path, "wb+") as autodoc_file:
            main_template.stream(app=self).dump(
                autodoc_file, encoding="UTF-8"
            )

        logger.opt(colors=True).success("Documentation was built in directory <c>{directory}</c>", directory=directory)


@dataclasses.dataclass
class Bot:
    app: App
    api: API
    events_factory: BaseEventFactory

    @classmethod
    async def via_token(cls, token: str, app: App) -> Bot:
        api = API(token)
        token_owner = await api.define_token_owner()
        events_factory: BaseEventFactory
        if token_owner is TokenOwner.USER:
            events_factory = UserLongPoll(api)
        else:
            events_factory = GroupLongPoll(api)
        return cls(app=app, api=api, events_factory=events_factory)

    async def run_polling(self):
        async for event in self.events_factory.listen():
            new_event_storage = NewEvent(event=event, bot=self)
            asyncio.create_task(self.handle_event(new_event_storage))

    async def handle_event(self, new_event_storage: NewEvent):
        # Запуск обработки события
        logger.opt(colors=True).info(
            "New event: <y>{event_type}</y>",
            event_type=new_event_storage.event.type,
        )
        asyncio.create_task(self.app.route_event(new_event_storage))

        if new_event_storage.event.type in {
            "message_new",
            "message_reply",
            4,
        }:
            message_storage = await NewMessage.from_event(
                event=new_event_storage.event, bot=new_event_storage.bot
            )

            asyncio.create_task(self.app.route_message(message_storage))

    async def close_sessions(self):
        await self.events_factory.close_session()
        await self.api.close_session()
