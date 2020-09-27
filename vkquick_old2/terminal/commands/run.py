import subprocess

import cleo
import watchdog


class Run(cleo.Command):
    """
    Run the bot

    run
        {--deploy : Отключение режима дебага и автоперезагрузки}
    """

    def handle(self):
        if self.option("deploy"):
            subprocess.run(
                ("python3.8", "-m", "src")
            )  # import src.__main__ ???
        else:
            ...
