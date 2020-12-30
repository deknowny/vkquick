import os
import sys

import cleo


class DebugRun(cleo.Command):
    """
    Запуск бота в режиме дебага, аналогично `watchgod src.__main__.run`

    debug-run
    """

    def handle(self):
        try:
            import watchgod
        except ImportError as err:
            raise ImportError(
                "Install `watchgod` for debug run (via pip)"
            ) from err
        run_command = f"watchgod src.__main__.run"
        os.system(run_command)


class ReleaseRun(cleo.Command):
    """
    Запуск бота с переменной окружения `VKQUICK_RELEASE=1` (деплойный запуск бота)

    release-run
    """

    def handle(self):
        run_command = f"{sys.executable} -m src"
        os.environ["VKQUICK_RELEASE"] = "1"
        os.system(run_command)
