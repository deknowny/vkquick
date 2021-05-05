Если вы уже работали с другими библиотеками для разработки под VK API (например, `vk_api` или `vk`), то скорее всего вы уже сталкивались с проблемой лишнего кода, чтобы банально отправить сообщение, нужно каждый раз писать `messages.send` и назначать `random_id` в случайное число или 0, а `peer_id` в `event.object.message.peer_id`. В общем, ужас. Команда, которая имеет несколько вариантов ответа разрастается до вселенских маштабов, и зачастую приходится писать свои функции-обертки, но в большинстве случаев работают они костыльно, поэтому __vkquick__ предлагает свое решение этой проблемы

## return-схема
Если вам нужно отправить сообщение в тот же самый диалог/беседу, откуда оно пришло — можете просто вернуть его. Помимо текста, можно вернуть `vq.Message`, который содержит в себе все поля метода `messages.send` и также автоматически выставляет `peer_id` в `event.object.message.peer_id`

!!! Example
    Просто ответить пользователю
    ```python
    return "Lorem ipsum"
    ```

!!! Example
    Вам нужно отключить пуш от упоминаний в сообщений, которое отпарвляете (тобишь кейс, где нужно передать некоторые поля `messages.send`)
    ```python
    return vq.Message(
        "Lorem ipsum and [id1|push]",
        disable_mentions=True
    )
    ```

## yield-схема
Предположим, что вы возвращаете какой-то список, и вместо того, чтобы складывать текст, вы можете просто yield'ить его.

!!! Example
    Список продуктов в столбик
    ```python
    import vkquick as vq


    @vq.Cmd(names=["fruits"])
    @vq.Reaction("message_new")
    def fruits():
        yield "Apple\n"
        yield "Orange\n"
        yield "Banana"
    ```
    Аналогично
    ```python
    import vkquick as vq


    @vq.Cmd(names=["fruits"])
    @vq.Reaction("message_new")
    def fruits():
        return "Apple\nOrange\nBanana"
    ```

!!! Example
    Возращает имена всех пользователей из пересланных сообщений
    ```python
    import vkquick as vq


    @vq.Cmd(names=["fdws"])
    @vq.Reaction("message_new")
    def fws_names(users: vq.FwdUsers()):
        for ind, user in enumerate(users, 1):
            yield f"{ind}) {user:<fn> <ln>}\n"
    ```
    Аналогично
    ```python
    import vkquick as vq


    @vq.Cmd(names=["fdws"])
    @vq.Reaction("message_new")
    def fws_names(users: vq.FwdUsers()):
        text = ""
        for ind, user in enumerate(users, 1):
            text += f"{ind}) {user:<fn> <ln>}\n"
        return text
    ```


!!! Note
    Вы не можете использовать yield вместе с `vq.Message` или return

## Отправка сразу
Вы также можете отправить сообщение внутри реакции сразу и продолжить выполнять какой-то код, предварительно используя `vq.Message()` как payload-тип

```python
import vkquick as vq


@vq.Reaction("message_new")
async def foo(answer: vq.Message()):
    """
    Отправит 3 сообщения
    """
    await answer("Lorem ipsum", disable_mentions=True)
    await answer("Ipsum lorem", keyboard=vq.Keyboard.empty())
    return vq.Message("Star it pls: https://github.com/Rhinik/vkquick")
```

Однако, вы все еще можете использовать "ручное" управление и отправить сообщение по старинке

```python
import vkquick as vq


@vq.Cmd(names=["hi"])
@vq.Reaction("message_new")
async def hello(api: vq.API, event: vq.Event()):
    await api.messages.send(
        peer_id=event.object.truncated_message.peer_id,
        message="hello",
        random_id=vq.random_id()
    )
    # Doing smth
```

!!! Tip
    Для сообщений, отправленных от лица пользователя (хотя vkquick не подразумевает создание юзерботов) вручную, можете использовать функцию `random_id`, опционально принимающая диапазон генерируемого `±`числа  

## Ответ на нажатие callback-кнопки
Вместо вызова `messages.sendMessageEventAnswer` вы можете использовать payload-аргумент `CallbackAnswer`. Вызовите метод, соответствующий типу события, которое должно случиться и передайте соответствующие аргументы

Всевозможные типы

* `show_snackbar`
* `open_link`
* `open_app`

принимает в себя соответствующие аргументы, требуемые для поля `event_data`

!!! Example
    ```python
    import vkquick as vq


    @vq.Reaction("message_event")
    async def callback_handler(
        cbanswer: vq.CallbackAnswer()
    ):
        await cbanswer.show_snackbar("Lorem ipsum")
    ```
