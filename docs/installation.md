Перед установкой необходимо удостовериться, что версия Python выше `3.7`:

<div class="termy">
```console
$ python -V
Python 3.7.0
```
</div>

***

Если необходимая версия есть, можно переходить к установке:

> До релиза 1.0: `python -m pip install -U https://github.com/deknowny/vkquick/archive/1.0.zip`

=== "PyPI"
    <div class="termy">
    ```console
    $ python -m pip install vkquick
    ---> 100%
    ```
    </div>

=== "GitHub"
    <div class="termy">
    ```console
    $ python -m pip install -U https://github.com/deknowny/vkquick/archive/master.zip 
    ---> 100%
    ```
    </div>

***

Проверьте, чтобы VK Quick установился корректно:
<div class="termy">
```console
$ python -m pip show vkquick
Name: vkquick
Version: ...
...
...
```
</div>

***

Вместе с фреймворком устанавливается `vq` — терминальная утилита (CLI), немного упрощающая создание ботов. Проверим и ее:

<div class="termy">
```console
$ vq --help
Usage: vq [OPTIONS] COMMAND [ARGS]...

Options:
...
...
```
</div>

!!! Tip
    CLI всегда можно запустить через вызов пакета: `python -m vkquick --help`
