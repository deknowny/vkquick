from __future__ import annotations

import asyncio
import dataclasses
import functools
import pathlib
import shutil
import typing

import jinja2
from loguru import logger

from vkquick.api import API, TokenOwner
from vkquick.base.event import BaseEvent
from vkquick.base.event_factories import BaseEventFactory
from vkquick.chatbot.exceptions import StopCurrentHandling, StopStateHandling
from vkquick.chatbot.package import Package
from vkquick.chatbot.storages import (
    CallbackButtonPressed,
    NewEvent,
    NewMessage,
)
from vkquick.event import GroupEvent
from vkquick.logger import update_logging_level
from vkquick.longpoll import GroupLongPoll, UserLongPoll

AppPayloadFieldTypevar = typing.TypeVar("AppPayloadFieldTypevar")


@dataclasses.dataclass
class App(Package, typing.Generic[AppPayloadFieldTypevar]):

    packages: typing.List[Package] = dataclasses.field(default_factory=list)
    debug: bool = False
    # Autodoc preferences
    name: str = "VK Quick Бот"
    description: str = "Чат-бот для ВКонтакте, написанный на Python с использованием VK Quick"
    site_title: str = "Документация к чат-боту"
    payload_factory: typing.Type[AppPayloadFieldTypevar] = dataclasses.field(
        default=None
    )

    def __post_init__(self):
        if self.debug:
            update_logging_level("DEBUG")

        packages_gen = self.packages.copy()
        for package in packages_gen:
            for command in package.commands:
                command.update_prefix(*self.prefixes)

        self.packages.append(self)

    @functools.cached_property
    def payload(self) -> AppPayloadFieldTypevar:
        return self.payload_factory()

    async def route_event(self, new_event_storage) -> None:
        routing_coroutines = [
            package.handle_event(new_event_storage)
            for package in self.packages
        ]
        await asyncio.gather(*routing_coroutines)

    async def route_message(self, ctx: NewMessage):
        try:
            if self.filter is not None:
                await self.filter.run_making_decision(ctx)
        except StopCurrentHandling:
            return
        else:
            routing_coroutines = [
                package.handle_message(ctx) for package in self.packages
            ]
            await asyncio.gather(*routing_coroutines)

    async def route_callback_button_pressing(
        self, ctx: CallbackButtonPressed
    ):
        routing_coroutines = [
            package.handle_callback_button_pressing(ctx)
            for package in self.packages
        ]
        await asyncio.gather(*routing_coroutines)

    def add_package(self, package: Package) -> None:
        self.packages.append(package)
        for command in package.commands:
            command.update_prefix(*self.prefixes)

    def run(
        self,
        *tokens: typing.Union[str, API],
        bot_payload_factory: typing.Optional[
            typing.Type[BotPayloadFieldTypevar]
        ] = None,
        build_autodoc: bool = True,
        docs_directory: str = "autodocs",
        docs_filename: str = "index.html"
    ) -> None:
        asyncio.run(
            self.coroutine_run(
                *tokens,
                bot_payload_factory=bot_payload_factory,
                build_autodoc=build_autodoc,
                docs_directory=docs_directory,
                docs_filename=docs_filename
            ),
            debug=self.debug,
        )

    async def coroutine_run(
        self,
        *tokens: typing.Union[str, API],
        bot_payload_factory: typing.Optional[
            typing.Type[BotPayloadFieldTypevar]
        ] = None,
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
            Bot.via_token(
                token=token, app=self, payload_factory=bot_payload_factory
            )
            for token in tokens
        ]
        bots = None
        try:
            bots = await asyncio.gather(*bots_init_coroutines)
            await self._call_startup(*bots)
            run_coroutines = [bot.run_polling() for bot in bots]
            await asyncio.gather(*run_coroutines)
        finally:
            if bots:
                await self._call_shutdown(*bots)
            for bot in bots:
                await bot.close_sessions()

    async def _call_startup(self, *bots: Bot) -> None:
        startup_coroutines = []
        for pkg in self.packages:
            for startup_handler in pkg.startup_handlers:
                for bot in bots:
                    startup_coroutines.append(startup_handler.handler(bot))

        await asyncio.gather(*startup_coroutines)

    async def _call_shutdown(self, *bots: Bot) -> None:
        shutdown_coroutines = []
        for pkg in self.packages:
            for shutdown_handler in pkg.shutdown_handlers:
                for bot in bots:
                    shutdown_coroutines.append(shutdown_handler.handler(bot))

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

        logger.opt(colors=True).success(
            "Documentation was built in directory <c>{directory}</c>",
            directory=directory,
        )


BotPayloadFieldTypevar = typing.TypeVar("BotPayloadFieldTypevar")


@dataclasses.dataclass
class Bot(typing.Generic[AppPayloadFieldTypevar, BotPayloadFieldTypevar]):
    app: App[AppPayloadFieldTypevar]
    api: API
    events_factory: BaseEventFactory
    payload_factory: typing.Type[BotPayloadFieldTypevar] = dataclasses.field(
        default=None
    )

    @functools.cached_property
    def payload(self) -> BotPayloadFieldTypevar:
        return self.payload_factory()

    @classmethod
    async def via_token(
        cls,
        *,
        token: typing.Union[str, API],
        app: App,
        payload_factory: typing.Optional[
            typing.Type[BotPayloadFieldTypevar]
        ] = None
    ) -> Bot:
        if isinstance(token, API):
            api = token
        else:
            api = API(token)
        token_owner, _ = await api.define_token_owner()
        events_factory: BaseEventFactory
        if token_owner == TokenOwner.USER:
            events_factory = UserLongPoll(api)
        else:
            events_factory = GroupLongPoll(api)
        return cls(
            app=app,
            api=api,
            events_factory=events_factory,
            payload_factory=payload_factory,
        )

    async def run_polling(self):
        async for event in self.events_factory.listen():
            logger.opt(colors=True).info(
                "New event: <y>{event_type}</y>",
                event_type=event.type,
            )
            new_event_storage = NewEvent(event=event, bot=self)
            asyncio.create_task(self.handle_event(new_event_storage))

    @logger.catch(exclude=StopStateHandling)
    async def handle_event(
        self, new_event_storage: NewEvent, wrap_to_task: bool = True
    ):
        route_event_coroutine = self.app.route_event(new_event_storage)
        if wrap_to_task:
            asyncio.create_task(route_event_coroutine)
        else:
            await route_event_coroutine

        if new_event_storage.event.type in {
            "message_new",
            "message_reply",
            4,
        } and (len(new_event_storage.event.content) > 3 or isinstance(new_event_storage.event, GroupEvent)):
            ctx = await NewMessage.from_event(
                event=new_event_storage.event,
                bot=new_event_storage.bot,
                payload_factory=new_event_storage.payload_factory,
            )

            route_message_coroutine = self.app.route_message(ctx)
            if wrap_to_task:
                asyncio.create_task(route_message_coroutine)
            else:
                await route_message_coroutine

        elif new_event_storage.event.type == "message_event":
            context = await CallbackButtonPressed.from_event(
                event=new_event_storage.event, bot=new_event_storage.bot
            )
            route_callback_button_pressing_coroutine = (
                self.app.route_callback_button_pressing(context)
            )
            if wrap_to_task:
                asyncio.create_task(route_callback_button_pressing_coroutine)
            else:
                await route_callback_button_pressing_coroutine

    async def close_sessions(self):
        await self.events_factory.close_session()
        await self.api.close_session()
