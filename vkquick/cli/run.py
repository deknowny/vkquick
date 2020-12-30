import os
import sys

import typer


run_typer = typer.Typer()


@run_typer.command()
def dev():
    try:
        import watchgod
    except ImportError as err:
        raise ImportError(
            "Install `watchgod` for debug run (via pip)"
        ) from err
    run_command = f"watchgod src.__main__.run"
    os.system(run_command)


@run_typer.command()
def release():
    run_command = f"{sys.executable} -m src"
    os.environ["VKQUICK_RELEASE"] = "1"
    os.system(run_command)