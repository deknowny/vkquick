До этого момента функции-обработчики наших реакций не имели никаких аргументов, однако, они это могут. Но вот вопрос — как `Reaction` узнает, чем должны быть аргументы и что вообще они могут содержать, да и в принципе, нужны ли они? Ответ ~~убил~~ прост — да, с помощью [аннотационных типов](https://www.python.org/dev/peps/pep-3107/) можно, например, получить объект сообщения, пользователя, отправившего это сообщения, список с фотографиями из сообщения, объект, позволяющий вызывать методы вк, вообще, что угодно, не проводя лишнюю возню с API. Допустим, мы хотим узнать время отправки сообщения, как это сделать? Перейдем к примеру

Создадим команду `get_time` в боте, а в `src/get_time/main.py` вставим следующее

```python
from datetime import datetime

import vkquick as vq


@vq.Reaction("message_new")
def get_time(event: vq.Event()):
    time = datetime.fromtimestamp(
        event.object.message.date
    )
    return f"Время отправки: {time:%H:%M}"
```

После чего запускаем бота через `$ bot run --reload --debug`, переходим к нему в лс и пишем любое сообщение, на что бот нам пришлет его время отправки. Вуа-ля!

Рассмотрим то, что мы написали в аргументах. Функция `get_time` принимает в свой единственный аргумент `event` объект [события нового сообщения](https://vk.com/dev/groups_events) (`message_new`), где в `event.object.message` хранится информация [о самом сообщении](https://vk.com/dev/objects/message), одно из полей которого — `date`, содержащее время отправки сообщения в [timestamp](https://ru.wikipedia.org/wiki/Unix-время). После чего с помощью модуля `datetime` мы превращаем datetime в human-вид, оставляя часы и минуты в процессе интерполяции в f-строку.

Нам потребовалось реализовать в логике всего пару физических строк, остальное взял на себя __vkquick__

!!! Note
    Обратите внимание на скобки у `vq.Event`. Для каждого payload-типа они __обязательны__, кроме нескольких исключений: `vq.API`, `vq.Bot` и аллиасные типы для аргументов текстовой команды, о которых речь пойдет позже

## Payload-типы из коробки
Каждый тип доступен из модуля через обращение по точке, т.е. `vq.Event`, `vq.Sender`

### `Event`
Возвращает объект пришедшего события. Само по себе событие это словарь, но с помощью [`attrdict`](https://pypi.org/project/attrdict/1.2.0/) вы можете получать ключи через точку. О всех событиях и их структуре можно почитать [здесь]((https://vk.com/dev/groups_events)). Не принимает аргументов при вызове

### `Sender`
Возвращает свой объект пользователя `vq.User`, отправившего сообщение, с _полями быстрого доступа_ и собственным форматированием. Принимает список \*аргсов для `fields` параметра в [`users.get`](https://vk.com/dev/users.get) и аргумент `name_case` для определения падежа имени и фамилии, тобишь `vq.Sender("bdate")` вернет пользователя

!!! Example
    Если написать боту `myname`, то он вернет имя пользователя, отправившего сообщение
    ```python
    import vkquick as vq


    @vq.Cmd(names=["myname"])
    @vq.Reaction("message_new")
    def get_name(sender: vq.Sender()):
        return sender.fn # fn это first_name
    ```

### `RepliedUser`
Возвращает пользователя `vq.User` из пересланного сообщения, если таковой имеется, иначе `None`. Принимает аналогичные для `Sender` поля

### `FwdUsers`
Возвращает __список__ из пользователей `vq.User`, попавших в пересланные сообщения (на самом верхнем уровне глубины). Переданные поля для `fields` и `name_case` добудутся для каждого из пользователей

### `ClientInfo`
Возвращает информацию о клиенте по доступным возможностям (может ли он работать с клаиватурой, с каруселями, какие кнопки поддерживает и прочее). Просто быстрый доступ к `event.object.client_info`

### `API` и `Bot`
Сессионные __объекты__, поэтому для того, чтобы получить их в аннотациях, скобки ставить не нужно. Их описание находится на отдельной странице

### `CallbackAnswer`
Используйте для ответа на нажатие callback-кнопки. Примеры использования есть в разделе [Быстрые ответы](./quick-answers.md)

### `GroupID`
Возращает ID группы из поля `group_id` пришедшего события. Такое же значение находится под полем `api.group_id.` в `config.toml`

### `ChatID`
ID чата. Для бесед `peer_id - 2_000_000_000`, для диалогов с пользователем или сообществом — ID пользователя/сообщества

### `PeerID`
ID диалога. Для бесед > 2_000_000_000

### `Message`
Используйте для отправки нескольких сообщений, либо выполнения какого-либо кода. Примеры использования есть в разделе [Быстрые ответы](./quick-answers.md)

## Кастомный тип
Для того, чтобы создать свой аннотационный тип, унаследуйтесь от базового класса для всех аннотаций `vq.Annotype`. После чего нужно будет переопределить абстрактный async/sync метод `prepare`. Именно он вызывается у payload-типа для определения значения аргумента. Метод принимает в себя следующие параметры:

Имя|Тип|Описание
:-|:-|:-
`argname`|str|Имя аргумента, на которое будет передано значение
`event`|vq.Event (почти тот же самый attrdict.AttrMap)|Объект события LongPoll
`func`|function/coroutine function|Функция-обработчик
`bin_stack`|type|Пустышка. Создается для каждого отдельного вызова какой-либо команды и живет пока происходит валидация, подготовка аннотипов и вызов обработчика. Используйте для своих каких-то дополнительных параметров, чтобы избежать гонку данных