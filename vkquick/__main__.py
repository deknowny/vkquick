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

from vkquick.cli.new import New
from vkquick.cli.run import DebugRun, ReleaseRun


app = cleo.Application()
app.add_commands(New(), DebugRun(), ReleaseRun())


if __name__ == "__main__":
    app.run()
