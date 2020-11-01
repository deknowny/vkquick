"""
Запуск CLI

Всю информацию можно найти по

    python -m vkquick -h

Либо по конкретной команде

    python -m vkquick new -h

Если с установкой все было в порядке, скрипт занесется в `PATH`
и вместо `python -m vkquick` можно писать `vq`
"""
import cleo

import vkquick.cli.new


app = cleo.Application()
app.add_commands(vkquick.cli.new.New())


if __name__ == "__main__":
    app.run()
