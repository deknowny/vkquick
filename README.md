__НА ДАННЫЙ МОМЕНТ ПРОДУКТ ВЕРСИИ 1.0 В РАЗРАБОТКЕ, ВСЯ ИНФОРМАЦИЯ НИЖЕ ЕЩЕ НЕ АКТУАЛЬНА. ПОДДЕРЖКИ 0.2 БОЛЬШЕ НЕТ, НО ВЫ ВСЕ ЕЩЕ МОЖЕТЕ УСТАНОВИТЬ ЕЕ С PYPI, НАЙТИ ДОКУМЕНТАЦИЮ НА [https://vkquick.github.io](https://vkquick.github.io) И ИСХОДНЫЙ КОД В ВЕТКЕ 0.2__
***
# VK Quick
[![Downloads](https://static.pepy.tech/personalized-badge/vkquick?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/vkquick)

__VK Quick — это современный асинхронный фреймворк для создания ботов ВКонтакте__

* [__Официальное сообщество в ВКонтакте__](https://vk.com/vkquick)

* [__Официальная беседа, где отвят на любой вопрос по API и разработке ботов__](https://vk.me/join/AJQ1dzLqwBeU7O0H_oJZYNjD)

* [__Официальный сайт с документацией__](https://vkquick.rtfd.io)

***

## Ключевые особенности:

* __Скорость__: VK Quick использует конкурентность в одном потоке (asyncio) и является одним из самых быстрых фреймворков для разработки ботов

* __Компактность кода__: Разработка требует меньше времени в несколько раз, код становится короче, вероятность возникновения багов уменьшается

* __Легкое обучение__: Создавать ботов невероятно просто вместе с VK Quick! Обучение проходит быстро и легко

* __Инструменты для упрощения разработки__: Из коробки VK Quick представляет два удобных инструмента — CLI (терминальная утилита) облегчающая разработку и Debugger — технологию интерактивного отображения состояния обработки каждой из команд для эффективной отладки

* __Поддержка актуального API__: Множество разных возможностей для ботов перенесены в удобный Python-стиль, любые нововведения в социальной сети незамедлительно отображаются в самом фреймворке

* __Отзывчивое коммьюнити__: Вы всегда можете обратиться с вопросом, на который обязательно ответят наши специалисты по разработке ботов в официальной беседе нашего сообщества

***

## Установка
Для начала нужно проверить версию Python:
```shell script
python -V
```
Если она выше, чем `3.7`, можно переходить к установке:

```shell script
python -m pip install vkquick
```

> До релиза 1.0: `python -m pip install git+https://github.com/Rhinik/vkquick@1.0`

Нужно проверить, корректно ли установился VK Quick:
```shell script
python -m pip show vkquick
```

Вместе с фреймворком устанавливается `vq` — терминальная утилита (CLI), немного упрощающая создание ботов. Проверим и ее:

```shell script
vq --help
```

> Если `vq` установился некорректно, можно запустить CLI через запуск самого пакета: `python -m vkquick --help`

Если установка прошла успешно, можно переходить к созданию самого простого бота

***

# Hello-бот
Для начала нам необходимо получить специальный токен — ключ, с помощью которого можно будет взаимодействовать с группой или аккаунтом пользователя

* Как получить токен для пользователя

* Как получить токен для группы и включить необходимые настройки для ботов

В качестве примера мы будем создавать бота именно для группы, но Вы всегда сможете просто подставить другой токен и писать бота уже для пользователя всё с тем же интерфейсом

```python
import vkquick as vq

bot = vq.Bot.init_via_token("your-token")


@bot.command(names="hi")
def hello():
    return "hello!"


bot.run()
```

Запускаем пример выше, подставляя токен. Теперь, если написать боту `hi` в личные сообщения, то он ответит нам `hello!`

> Бот также будет работать в любой беседе, но для этого необходимо в беседе выдать боту права администратора или полного доступа к переписке

Хотите больше возможностей? Переходите на наш официальный сайт [https://vkquick.rtfd.io](https://vkquick.rtfd.io) и продолжайте углубляться в разработку ботов вместе с VK Quick!
