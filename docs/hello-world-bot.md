
После процесса [установки](installation.md) мы можем попробовать написать своего первого бота. Поехали!

Еще раз разберемся с тем, что у нас есть:

1. Сам модуль, содержащий множество разных инструментов
1. Терминальная команда `bot`, представляющая из себя некого _менеджера_ всех ваших ботов

## Новый бот
Для начала, давайте создадим проект бота и сразу перейдем в его директорию

<!--
Colorfull output

<div class="termy">
```console
$ bot new hello_world
<span style="color: YellowGreen;">Created <span style="color: Cyan;">hello_world</span> bot. Don't forget `cd` to bot's directory</span>

<span style="color: Yellow;">Please, add following parameters to <span style="color: Cyan;">hello_world/config.toml</span> under <span style="color: Cyan;">[api]</span> section</span>
 -- <span style="color: Red;">token</span>
 -- <span style="color: Red;">group_id</span>

$ cd hello_world
```
</div> -->
<div class="termy">
```console
$ bot new hello_world
Created hello_world bot. Don't forget `cd` to bot's directory

Please, add following parameters to hello_world/config.toml under [api] section
 -- token
 -- group_id

$ cd hello_world
```
</div>

## Настройка конфига
Теперь нужно указать токен и ID группы, от лица которой будет работать бот, в файле `config.toml` под заголовком `[api]`. Их нужно вставить под соответствующие переменные

```toml hl_lines="2 3"
[api]
token = ""
group_id = 0
owner = "group"
version = 5.124


[longpoll]
wait = 25
```

Получиться должно что-то в этом роде

```toml
[api]
token = "4c491a152bd3163c2e1162541c1e821a665706213490a56acf8a58fbc9c0515dc96a6e3b2da5ba1201d57"
group_id = 192978547
owner = "group"
version = 5.124


[longpoll]
wait = 25
```

!!! Tip
    ID Группы можно узнать [здесь](https://regvk.com/id/)

!!! Tip
    Вы можете сразу указать токен и ID группы при создании бота через флаги `-t` и `-gi`. Мы также советуем сразу обозначать владельца бота (флаг `-o`), который заносится как правообладатель в лицензию, то есть
    ```console
    $ bot new -o "Vladimir Putin" -gi 192978547 -t 4c491a152bd3163c2e1162541c1e821a665706213490a56acf8a58fbc9c0515dc96a6e3b2da5ba1201d57
    ```

## Создание команды
Теперь можно сделать примиивную команду — мы пишем боту `hello`, а он нам отвечает. Команды также создаются через терминал
<div class="termy">
```console
$ bot com hello
Added a command hello into path src/hello
```
</div>

## Запуск
Штош, можно запускать!
<div class="termy">
```console
$ bot run --reload --debug
Listen
```
</div>

Переходим в лс боту и пишем `hello`. Вуа-ля! А ведь вы еще не написали _ни одной_ строчки на Python...
