# Установка
Установить фреймворк можно следующей командой

=== "GitHub"
    <div class="termy">
    ```console
    $ python -m pip install -U https://github.com/deknowny/vkquick/archive/master.zip 
    ---> 100%
    ```
    </div>


=== "PyPI"
    На `PyPI` будет загружена стабильная версия. Сейчас продукт все еще в разработке
    <!--
    <div class="termy">
    ```console
    $ python -m pip install -U https://github.com/deknowny/vkquick/archive/1.0.zip
    ---> 100%
    ```
    </div>-->
    
***

## Ошибки при установке
Если у вас появляются ошибки при установке, попробуйте следующее
***
Проверьте, версия вашего `python` выше `3.8`
<div class="termy">
```console
$ python -V
Python 3.8.2
```
</div>

***
Обновите версию `pip` до последней
<div class="termy">
```console
$ python -m pip install --upgrade pip
---> 100%
```
</div>

***
Установите `poetry` самостоятельно
<div class="termy">
```console
$ python -m pip install poetry
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
Процесс установки производится единожды. Теперь все необходимые зависимости установлены и готовы к использованию