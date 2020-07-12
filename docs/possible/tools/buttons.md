> Кнопки совместимы и с, `Keyboard`, и с `Element`

## Разные типы
Кнопки существуют 6 разных типов, о которых можно почитать [здесь](https://vk.com/dev/bots_docs_3?f=4.2.%20Структура%20данных). Для того, чтобы создать одну из кнопок такого вида, вызовите соответствующий статический метод, а в скобках передайте нужные параметры для содержимого поля `action` у кнопки:

* `vq.Button.text()`
* `vq.Button.open_link()`
* `vq.Button.location()`
* `vq.Button.vkpay()`
* `vq.Button.open_app()`
* `vq.Button.callback()`

---

Если кнопка содержит поле `text`, его можно указать без ключа

`vq.Button.text("Lorem ipsum")`

Эквивалнтно

`vq.Button.text(text="Lorem ipsum")`

---

Если кнопка содержит параметр `payload` — можете передать в него словарь, а не строку. __vkquick__ автоматически преобразует этот словарь в JSON формат, т.е. следующие кнопки валидны

`vq.Button.text("foo", payload={"text": "foo"})`

Эквивалнтно

`vq.Button.text("foo", payload='{"text": "foo"}')`

---

Если кнопка может быть разных цветов, вызовите метод с соответсвующим цветом

* `vq.Button.text("Lorem ipsum").primary()`
* `vq.Button.text("Lorem ipsum").secondary()`
* `vq.Button.text("Lorem ipsum").positive()`
* `vq.Button.text("Lorem ipsum").negative()`

---
Кнопку можно создать по словарю

```python
vq.Button.by(
    {
        "action": {
            "type": "text",
            "label": "Lorem ipsum"
        },
        "color": "primary"
    }
)
```

Что эквивалетно

`vq.Button.text("Lorem ipsum").primary()`

---
После чего кнопку можно передать в один из конструкторов

---
Содержимое кнопки (словарь) хранится в поле `info`
