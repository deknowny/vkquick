## PyPI
Вы можете установить `vkquick` с помощью `pip`
<div class="termy">
```console
$ pip install vkquick
---> 100%
```
</div>

## GitHub
Либо же произвести установку через исходники на [GitHub](https://github.com/Rhinik/vkquick)

=== "Linux, MacOS"
    <div class="termy">
    ```console
    $ git clone https://github.com/Rhinik/vkquick
    $ cd vkquick
    $ python3 -m venv env
    $ source env/bin/activate
    $ pip3 install poetry
    $ poetry install --no-dev
    ```
    </div>

=== "Windows (cmd)"
    <div class="termy">
    ```console
    $ git clone https://github.com/Rhinik/vkquick
    $ cd vkquick
    $ python -m venv env
    $ env\Scripts\activate.bat
    $ pip install poetry
    $ poetry install --no-dev
    ```
    </div>

## Check it
После установки будет доступен как сам фреймворк, так и терминальный инструмент __bot__. Проверьте корректность установки

<div class="termy">
```console
$ bot --help
Usage: bot [OPTIONS] COMMAND [ARGS]...

  Менеджер Ваших ботов
...
...
...

$ python
>>> import vkquick
>>>
```
</div>
