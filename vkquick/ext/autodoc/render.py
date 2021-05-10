import os
import pathlib

import jinja2

from vkquick.ext.chatbot.application import App


def render_autodoc(
    app: App, directory: str = "site", filename: str = "index.html"
):
    autodoc_dir = os.path.abspath(os.path.dirname(__file__))
    current_templates = os.path.join(autodoc_dir, "templates")
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(current_templates)
    )
    main_template = env.get_template("index.html")

    saved_path_dir = pathlib.Path(directory)
    saved_path_dir.mkdir(parents=True, exist_ok=True)
    saving_path = saved_path_dir / filename
    with open(saving_path, "w+") as autodoc_file:
        main_template.stream(app=app, print=print).dump(autodoc_file)
