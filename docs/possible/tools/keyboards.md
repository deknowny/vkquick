Вы можете отправить [клавиатуру в сообщении](https://vk.com/dev/bots_docs_3?f=4.%20Клавиатуры%20для%20ботов), используя лишь корректно составленный словарь и `json.dumps`

```python
import json

import vkquick as vq


@vq.Cmd(names=["kb"])
@vq.Reaction("message_new")
def kb():
    keyboard_scheme = {
        "one_time": True,
        "inline": False,
        "buttons": [
            [
                {
                    "action": {
                        "type": "text",
                        "label": "Left button"
                    },
                    "color": "positive"
                },
                {
                    "action": {
                        "type": "text",
                        "label": "Right button"
                    },
                    "color": "negative"
                }
            ],
            [
                {
                    "action": {
                        "type": "text",
                        "label": "Buttom button"
                    },
                    "color": "primary"
                }
            ]
        ]
    }
    return vq.Message(
        "Simple keyboard",
        keyboard=json.dumps(keyboard_scheme, ensure_ascii=False)
    )
```

Либо используя автодамп

```python
import vkquick as vq


@vq.Cmd(names=["kb"])
@vq.Reaction("message_new")
def kb():
    keyboard_scheme = {
        "one_time": True,
        "inline": False,
        "buttons": [
            [
                {
                    "action": {
                        "type": "text",
                        "label": "Left button"
                    },
                    "color": "positive"
                },
                {
                    "action": {
                        "type": "text",
                        "label": "Right button"
                    },
                    "color": "negative"
                }
            ],
            [
                {
                    "action": {
                        "type": "text",
                        "label": "Buttom button"
                    },
                    "color": "primary"
                }
            ]
        ]
    }
    return vq.Message(
        "Simple keyboard",
        keyboard=vq.Keyboard.by(keyboard_scheme)
    )
```

Либо используя один из методов конструктора (рекомендуемо из-за своей краткойсти и читабельности)

=== "Задавая сразу все кнопки"
    ```python
    import vkquick as vq


    @vq.Cmd(names=["kb"])
    @vq.Reaction("message_new")
    def kb():
        keyboard = vq.Keyboard(one_time=True).generate(
            vq.Button.text("Left button").positive(),
            vq.Button.text("Right button").negative(),
            vq.Button.line()
            vq.Button.text("Buttom button").primary(),
        )

        return vq.Message(
            "Simple keyboard",
            keyboard=keyboard
        )
    ```

=== "Задавая кнопки поэтапно"
    ```python
    import vkquick as vq


    @vq.Cmd(names=["kb"])
    @vq.Reaction("message_new")
    def kb():
        keyboard = vq.Keyboard(one_time=True)
        keyboard.add(vq.Button.text("A Button!").positive())
        keyboard.add(vq.Button.text("Right button").negative())
        keyboard.add(vq.Button.line())
        keyboard.add(vq.Button.text("Buttom button").primary())

        return vq.Message(
            "Simple keyboard",
            keyboard=keyboard
        )
    ```


## `Keyboard`
Создает кливиатуру 3мя способами:

1. По словарю, соответствующему [JSON схеме клавиатуры](https://vk.com/dev/bots_docs_3?f=4.3.%2BОтправка%2Bклавиатуры) через метод `by`, принимающий этот словарь

2. С помощью метода `generate`, принимающий в себя \*список кнопок и `vq.Button.line()`'ов

3. Поэтапно каждую кнопку и линию через метод `add`, принимающий 1 кнопку/новую линию

После чего вы можете передать объект в поле `keyboard` в классе `Message`

Основная информация о словаре клавиатуры хранится в поле `info`

!!! Note
    Dumps объекта происходит в \_\_repr\_\_, поэтому вы также можете просто передать объект и в ручном вызове `messages.send`
