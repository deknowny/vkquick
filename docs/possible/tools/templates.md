Чтобы создать [карусель](https://vk.com/dev/bot_docs_templates?f=5.%2BШаблоны%2Bсообщений), вам нужно сделать соответствующий генератор его элементов

!!! Question
    Если вы не знакомы с терминами `генератор` и `yield`, ознакомиться можно [здесь](https://habr.com/ru/post/132554/)

```python
import vkquick as vq


@vq.Cmd(names=["tp"])
@vq.Reaction("message_new")
def tp():
    return vq.Message(
        "Your template",
        template=carousel()
    )

@vq.Template()
def carousel():
    titles = ["Foo", "Bar"]
    descs = ["Foo desc", "Bar desc"]
    kbs = [
        [vq.Button.text("foo")],
        [vq.Button.text("bar")]
    ]
    for title, desc, kb in zip(
        titles, descs, kbs
    ):
        elem = vq.Element(
            title=title,
            description=desc,
            buttons=kb
        )
        yield elem.open_link("https://google.com")
```
## Шаг 1: Создайте генератор
Поскольку элементы карусели одношаблонны (т.е. выглядят одинаково), то нам достаточно просто пройтись циклом по нужным заголовкам, описаниям, клавиатуре и фотографиям (если таковые имеются). Поэтому для начала создаем саму функцию, которая, к слову, может что-то принимать. Аргументы, которые вы хотите добавить в нее, используйте при вызове (пример такого кейса в самом низу)

```python hl_lines="1 2"
@vq.Template()
def carousel():
    titles = ["Foo", "Bar"]
    descs = ["Foo desc", "Bar desc"]
    kbs = [
        [vq.Button.text("foo")],
        [vq.Button.text("bar")]
    ]
    for title, desc, kb in zip(
        titles, descs, kbs
    ):
        elem = vq.Element(
            title=title,
            description=desc,
            buttons=kb
        )
        yield elem.open_link("https://google.com")
```

Вы также можете конкретно указать тип шаблона. По умолчанию он `"carousel"`
```python hl_lines="1 2"
@vq.Template(type_="carousel")
def carousel():
    ...
```

## Шаг 2: Соберите данные для элементов
Ваша задача — сделать yield элементов карусели. Что для этого нужно? Алгоритмом в примере мы создаем список заголовков, описаний и __клавиатур__ (здесь без `Keyboard`, только список `Button`'ов). После чего проходимся `for`'ом по `zip`'ованным спискам (на каждый n-ный элемент списка возвращается кортеж из всех)

```python hl_lines="3-11"
@vq.Template()
def carousel():
    titles = ["Foo", "Bar"]
    descs = ["Foo desc", "Bar desc"]
    kbs = [
        [vq.Button.text("foo")],
        [vq.Button.text("bar")]
    ]
    for title, desc, kb in zip(
        titles, descs, kbs
    ):
        elem = vq.Element(
            title=title,
            description=desc,
            buttons=kb
        )
        yield elem.open_link("https://google.com")
```

## Шаг 3: Создаем объект элемента
После того, как мы получили данные для каждого из элементов — создаем соответствующий инстанс

```python hl_lines="12-16"
@vq.Template()
def carousel():
    titles = ["Foo", "Bar"]
    descs = ["Foo desc", "Bar desc"]
    kbs = [
        [vq.Button.text("foo")],
        [vq.Button.text("bar")]
    ]
    for title, desc, kb in zip(
        titles, descs, kbs
    ):
        elem = vq.Element(
            title=title,
            description=desc,
            buttons=kb
        )
        yield elem.open_link("https://google.com")
```

## Шаг 4: Назначаем действие
Элемент имеет одно из следующих действий:

* open_link
* open_photo

Поэтому нужно вызвать соответсвующий метод (у меня при нажатии на элемент открывается страница гугла)
```python hl_lines="17"
@vq.Template()
def carousel():
    titles = ["Foo", "Bar"]
    descs = ["Foo desc", "Bar desc"]
    kbs = [
        [vq.Button.text("foo")],
        [vq.Button.text("bar")]
    ]
    for title, desc, kb in zip(
        titles, descs, kbs
    ):
        elem = vq.Element(
            title=title,
            description=desc,
            buttons=kb
        )
        yield elem.open_link("https://google.com")
```

## Шаг 5: yield Элемента
Последним этапом нам нужно `yield`'нуть элемент

## Шаг 6: Вызов карусели
Теперь нам нужно лишь вызвать карусель и ее можно прикреплять к полю `template` в классе `Messsage`

```python hl_lines="3"
return vq.Message(
    "Your template",
    template=carousel()
)
```


Вы также можете создать карусель через метод `by`, передав туда словарь, [описывающий схему карусели](https://vk.com/dev/bot_docs_templates?f=5.1.%2BКарусели)


!!! todo
    Планируется сделать еще более упрощенный генератор каруселей, которому нужно будет лишь скармливать списки

!!! Note
    На момент напсиания статьи карусели поддерживаются только в мобильных клиентах. На веб версии вк такого функционала еще нет

!!! Example
    Карусель с принимаемым заголовками из текста пользователя (пример использования аргуменов)
    ```python
    import vkquick as vq


    @vq.Cmd(names=["tp"])
    @vq.Reaction("message_new")
    def tp(titles: vq.List(vq.Word, min_=2, max_=2)):
        return vq.Message(
            "Your template",
            template=carousel(titles)
        )

    @vq.Template()
    def carousel(titles):
        descs = ["Foo desc", "Bar desc"]
        kbs = [
            [vq.Button.text("foo")],
            [vq.Button.text("bar")]
        ]
        for title, desc, kb in zip(
            titles, descs, kbs
        ):
            elem = vq.Element(
                title=title,
                description=desc,
                buttons=kb
            )
            yield elem.open_link("https://google.com")
    ```

Содержимая схема в виде словаря находится в поле `info`
