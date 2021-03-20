Загрузка документов может происходить для двух направлений

* В сообщение (статический метод `message`)
* На стену (Статический метод `wall`)

Каждый из этих методов принимает соотвествующие аргументы для методов, получающих `upload_url` (аналогично загрузчкиу фотографий), и принимает поле `file`, представляющее собой одно из следующих инстансов:

1. `BytesIO`/`TextIOWrapper` объект
2. Поток байтов/строка
3. `pathlib.Path` до файла

После нужно вызвать корутинный метод `__call__`, передав параметры для соответствующего VK API метода `.save`. В ответ вы получите объект, хранящий VK API'шный объект документа аналогично объекту `Photo` (с теми же полями и возможностями)

!!! Example
    Загрузка документа в сообщение
    ```python
    from pathlib import Path

    import vkquick as vq


    @vq.Cmd(names=["send doc"])
    @vq.Reaction("message_new")
    async def doc(event: vq.Event()):
        doc = await vq.Doc.message(
            file=Path("example.txt"),
            peer_id=event.object.message.peer_id,
            type_="doc"
        )()

        return vq.Message(attachment=doc)
    ```
