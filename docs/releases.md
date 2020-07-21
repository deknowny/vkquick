### 0.2.6

Пофикшены callback кнопки -- теперь к ним можно применять цвета. В некоторых местах подрефакторен код

### 0.2.5

Пофикшены некоторые очепятки в докстрингах. Убраны неиспользуемые модули для некоторых файлов

### 0.2.4

Пофикшен баг при обработке LongPoll ошибок, добавленны некоторые комментарии в код. x.x.X обновления теперь вместо `<h2>` стали `<h3>`

### 0.2.3

Исправлены некоторые опечатки, усовершенствован алгоритм замены snake_case на CamelCase

### 0.2.2

Пофикшен запуск через `bot run`

### 0.2.1

Добавлен black в качестве форматтера кода. Убраны иниты из ChatOnly и DirectOnly

## 0.2.0
* Появилась полная поддержка callback-кнопок, включая payload-тип `CallbackAnswer` для быстрой отправки по методу `messages.sendMessageEventAnswer` вместо ручного API запроса

```python
import vkquick as vq

from . import config


@vq.Reaction("message_event")
async def callback_handler(
    cbanswer: vq.CallbackAnswer()
):
    await cbanswer.show_snackbar("Lorem ipsum")
```

* В сигналах появилась поддержка возвращаемых значений. Теперь сигналом можно  вернуть что-то и использовать это значение у себя в реакции или другом сигнале
* classmethod `empty()` для класса `vq.Keyboard`, чтобы создать пустую клавиатуру
* name_case в payload-типах (`Sender`, `RepliedUser`...)
* Новые payload типы
    * GroupID
    * ChatID
    * PeerID

* Новые Cmd-типы
    * Custom
    * Optional

* Новые валидаторы
    * ChatOnly
    * DirectOnly

* Поле `api.URL` в `config.toml` для своего URL под вызов методов
* Корутинная функция `vq.signal` для вызова сигнала вместо `vq.current.bot.signals.resolve`
* `vq.Message` теперь также поддерживает расположение в payload-типах. Можно отправлять сообщение неограниченное количество раз, используя все поля `messages.send`, сохраняя совместимость с прошлым способом отправки

```python
import vkquick as vq


@vq.Reaction("message_new")
async def foo(answer: vq.Message()):
    await answer("Lorem ipsum", disable_mentions=True)
    await answer("Ipsum lorem", keyboard=vq.Keyboard.empty())
    return vq.Message("Star it pls: https://github.com/Rhinik/vkquick")
```

Код выше отправит 3 сообщения

* Добавлены некоторые поля в описание проекта для PyPI (классификаторы, дополнительные ссылки...)

## 0.1.0
* [__Наша официальная группа ВК__](https://vk.com/vkquick)
* [__Беседа, в которой ответят на любой Ваш вопрос по vkquick и API в целом__](https://vk.me/join/AJQ1dzLqwBeU7O0H_oJZYNjD)
* [__Документация__](https://rhinik.github.io)
