"""
## Установка
С первым _стабильным_ релизом установка будет происходить через
```
$ pip install vkquick
```
Сейчас же попробовать ```vkquick``` можно через гайд в README на
[странице проекта GitHub](https://github.com/Rhinik/vkquick)
## Hello world
Пример _hello world_ бота (не забудьте указать свой токен и ID группы)
```
$ bot new mybot -o Bob -t abdef23ab -gi 456334534
$ cd mybot
$ bot com hello
$ but run --reload --debug
```
Теперь можете написать боту `hello` и уже получить ответ!  А ведь вы даже еще не написали ни одной строчки на Python...
## Из чего состоит директория бота
На данный момент папка с ботом выглядит как-то так:
```
├── LICENSE
├── README.md
├── config.toml
└── src
    ├── __init__.py
    └── hello
        ├── __init__.py
        ├── config.py
        └── main.py
```
### LICENSE
Обычный лицензионный файл с MIT лицензией.
Правообладатель сразу указывается из _опционального_ флага `-o` в команде `$ bot new`

### README.md
Классика любого проекта. Добавляйте сюда информацию о своем боте,
причем как по использованию,
так и для разработки
(хотя второе можно вынести в ```CONTRIBUTING.md```)

### config.toml
В нем располагаются абсолютно все настройки вашего бота,
начиная токеном, заканчивая настройками дебага.
Если Вы не знакомы с файлами формата TOML,
то Вам [сюда](https://github.com/toml-lang/toml)

О возможных парамтреах этого конфига можно узнать в `config_toml`

### src/
В этой папке содержатся все команды
и хендлеры сигналов, которые вы создаете,
да и в принципе абсолютно весь код бота. Каждая команда представляет собой пакет из трех файлов. Вам важны лишь два:

* ```main.py``` -- сам код команды
* ```config.py``` -- конфиг __для команды__

```__init__.py``` как в ```src/```, так и в папке команды заполняется автоматически

## Команды (Reactions)

### Терминал
Команда создается следующим образом:
```
$ bot com <name>
```
Это сделает следующее:

1. Создаст пакет внутри ```src```,
где внутри ```main.py``` будет находиться
__одноименная__ функция, представляющая собой команду
1. Заимпортирует Вашу функцию (команду) в ```src/__init__.py```
1. Внутри ```config.py``` будет создан
примитивный ответ с именем команды,
которая вызывается по тому же самому имени

Если вы хотите переименновать команду, используйте

<добавлю позже>

Для удаления используйте фалг ```-d```:
```
$ bot com -d <name>
```
Это автоматически удалит папку с командой и сотрет импорт в ```src/__init__.py```

### ```main.py```
Cейчас он выглядит вот так
```python
import vkquick as vq

from . import config


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
def hello():
    \"""
    Handler to command "hello"
    \"""
    return config.ANSWER
```
По порядку

1. ```import vkquick as vq```

    ```from . import config```

    Думаю, тут все ясно

1. `@vq.Cmd(names=config.NAMES)`

    __Валидатор__ `validators.cmd.Cmd` Указывает, каким образом
    должна обрабатываться команда.
"""

from .api import API
from .bot import Bot
from .exception import VkErr
from .lp import LongPoll
from .signal import Signal, SignalsList
from .reaction import Reaction, ReactionsList

from .annotypes import *
from .validators import *
from .tools import *


__version__ = "0.1.0a1"
