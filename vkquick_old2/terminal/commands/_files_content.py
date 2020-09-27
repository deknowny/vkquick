LICENSE = """
Copyright (c) {year} {owner}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""".strip()


README = """
# {name}
![VK API library](https://bit.ly/3gdTRLC)

VK Bot. In developing now.
""".strip()


CONFIG = '''
import typing as ty

import vkquick_old2 as vq
import attrdict


class API:
    """
    Конфигурация для API запросов
    """

    token: str = "abc"
    """
    Access token пользователя/группы
    """

    version: ty.Union[str, float] = 5.124
    """
    Версия API
    """

    owner: vq.TokenOwner = vq.TokenOwner.GROUP
    """
    Владелец токена -- группа или пользователь.
    Если владельцем является пользователь, то требуется
    передать ID группы в `group_id` для LongPoll настроек
    """

    response_factory: ty.Callable[[dict], ty.Any] = attrdict.AttrMap
    """
    Обертка для ответов от API запросов. `attrdict.AttrMap`
    Позволяет получать значения словаря (ответа) через точку
    """

    URL: str = "https://api.vk.com/method/"
    """
    URL для отправки API запросов
    """


class LongPoll:
    """
    Конфигурация для работы с LongPoll
    """

    wait: int = 25
    """
    Время максимального ожидания ответа
    """


class Debugger:
    """
    Конфигурация для работы дебаггера
    """

    @staticmethod
    def filter_showing(event: vq.Event):
        """
        Вызывается перед выводом информации в дебаггере.
        Если фозвращается `False`, то событие игнорируется
        и информации о нем отображаться не будет
        """
        return True


class Docs:
    """
    Конфигурация для создания документации
    """

    output_dir = "docs"
    """
    Директория, где будет располагаться автоматически
    сгенерированная документация
    """
'''.strip()


MAIN = """
import vkquick_old2 as vq

import src
import config


bot = vq.Bot.from_config(config.Bot)
api = vq.API.from_config(config.API)
longpoll = vq.LongPoll.from_config(config.LongPoll)

signals, reactions = vq.filter_src_content(src)
bot.reactions = reactions
bot.signals = signals

vq.current.api = api
vq.current.bot = bot
vq.current.longpoll = longpoll


if __name__ == "__main__":
    bot.run()
""".strip()
