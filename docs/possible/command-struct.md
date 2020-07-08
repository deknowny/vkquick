!!! Info
    Команда в __vkquick__ — вещь очень неоднозначная. Это хендлер реакций, целый набор _валидаторов_, _payload-аргументы_ и много мелких деталей. Здесь мы разберем файловую структуру и немного затронем код, чтобы чуть-чуть понимать, что вообще из себя представляет команда, а дальше уже копнем более конкретно

Команды создаются через терминал

<div class="termy">

```console
$ bot com some_name
Added a command some_name into path src/some_name
```
</div>

И состоят из 3х файлов:

## `main.py`

Содержит весь основной код, обрабатывающий команды, выраженный функцией с некой "пачкой" декораторов, обычно, с возвращаемым значеним и, возможно, какими-то аргументами. Сам код команды стоит разобрать на примемере, поэтому создайте нового бота (`$ bot new <name>`), либо выберите существующего и сделайте в нем команду `hello` (`$ bot com hello`), после чего откройте файл `src/hello/main.py`, именно его содержание мы сейчас разберем, чтобы привыкнуть к стилю кода

---

Думаю, насчет импортов все понятно. О `config.py` речь пойдет чуть ниже

```python hl_lines="1 3"
import vkquick as vq

from . import config


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
def hello():
    """
    Handler to command "hello"
    """
    return config.ANSWER
```

__Cmd__ — _валидатор_ (о них позже), в котором мы указываем, из каких имен и префиксов состоит команда, должна ли она быть чувствительна к регистру, что из себя представляют ее аргументы и другие настройки.

```python hl_lines="6"
import vkquick as vq

from . import config


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
def hello():
    """
    Handler to command "hello"
    """
    return config.ANSWER
```

__Reaction__ — хэндлер [LongPoll событий](https://vk.com/dev/groups_events). `"message_new"` говорит о том, что команда реагирует на событие нового сообщения
```python hl_lines="7"
import vkquick as vq

from . import config


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
def hello():
    """
    Handler to command "hello"
    """
    return config.ANSWER
```

Сам обработчик команды при ее вызове пользователем представляет собой sync/async функцию. Пока что в ней нет аргументов, но это тоже отдельная тема
```python hl_lines="8"
import vkquick as vq

from . import config


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
def hello():
    """
    Handler to command "hello"
    """
    return config.ANSWER
```

Возвращая что-то, мы как бы отвечаем пользователю. В нашем случае возвращается текст из `config.py`
```python hl_lines="12"
import vkquick as vq

from . import config


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
def hello():
    """
    Handler to command "hello"
    """
    return config.ANSWER
```

!!! Tip
    По умолчанию команда реагирует на свое имя, с которым вы ее создали. То есть `$ bot new foo` создает команду, реагирующую на `foo` в сообщении


## `config.py`
_Изменяемые_ настройки вашей команды. Всегда старайтесь выносить сюда имена, префиксы и прочее литеральные значения. Однако, вы можете обойтись и без этого файла, но мы рекомендуем вам стараться располагать все данные о конфигурации команды именно сюда. Почему? Вы вряд ли будете менять логику обработки, а вот какие-то ее параметры — вполне возможно. Заметьте, что здесь должны находиться настройки только для 1 команды, тобишь для той, для которой была выделена директория. Если вы хотите задать какой-то параметр, который легко будет доступен среди всех ваших команд (например, все ваши команды начинаются с одного и того же префикса), используйте `config.toml`, который можно получить через `vkquick.current.bot.config`.

## `__init__.py`
Сюда происходит импорт вашей команды, но вы также могли заметить, что она импортируется и в `src/__init__.py`, и поэтому, чтобы перименновать или удалить команду _чисто_, т.е. не оставляя лишних некорректных импортов, используйте соотвествующие флаги `-r` и `-d`

<div class="termy">

```console
$ bot com some_name -r new_name
Command some_name renamed to new_name

$ bot com new_name -d
Command foo will be removed. Continue? (y/any) y
Command foo has been removed
```
</div>

!!! todo
    Планируется добавить автогенератор документации по вашему коду, но как именно — пока еще не решено. Единственное, что могу сказать точно — она будет сделана под [MKDocs Material](https://squidfunk.github.io/mkdocs-material/), как сделан и этот сайт. Надеюсь, стилистически он вам нравится :D
