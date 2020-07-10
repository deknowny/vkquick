## Установка
1. Установите репозиторий из ветки __0.1__ к себе
2. Зайдите в появивишуюся директорию (__vkquick__)
3. Создайте виртуальное окружение
4. Установите туда [poetry](https://github.com/python-poetry/poetry)
5. Прозведите установку всех зависимостей

=== "Linux/MacOS"
    <div class="termy">
    ```console
    $ git clone -b 0.1 https://github.com/Rhinik/vkquick/
    $ cd vkquick
    $ python3 -m venv env
    $ source env/bin/activate
    $ pip3 install poetry
    $ poetry install
    ```
    </div>

=== "Windows (cmd)"
    <div class="termy">
    ```console
    $ git clone -b 0.1 https://github.com/Rhinik/vkquick/
    $ cd vkquick
    $ python -m venv env
    $ env\Scripts\activate.bat
    $ pip install poetry
    $ poetry install
    ```
    </div>

## Тесты
1. Откройте файл `tests/test_bot/config_example.toml` и перенесите его содержимое в новый файл `tests/test_bot/config.toml`. Вам нужно указать в новом файле следующие поля
    * `api.token`: Токен от группы, в котором запустится тестовый бот
    * `api.group_id`: ID группы, в котором запустится тестовый бот
    * `tests`: peer_id чата, который вы должны создать и в который пригласить вашего бота-тестировщика
    * `user_token`: Токен от __вашего__ акаунта, который находится в беседе с ботом


2. Запустите тесты следующей командой

<div class="termy">
```console
$ pytest tests -s
```
</div>

После чего вы можете наблюдать некое "общение" вашего аккаунта с ботом. Проследите, чтобы бот ответит на каждую команду. Вы также можете интерактивно наблюдать состояния обработки команд в терминале. Проскроллив вверх можно увидеть пришедшеее LongPoll событие.


В случае, если какая-то команда не сработала, вы можете запустить бота в обычном режиме и протестировать какую-то команду вручную

<div class="termy">
```console
$ python3 tests/test_bot/test_run.py
```
</div>
