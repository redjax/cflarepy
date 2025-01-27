from loguru import logger as log

import settings

from cyclopts import App, Group, Parameter
from .clean import cleanup_app


MOUNT_SUBAPPS: list[App] = [cleanup_app]

project_app = App(name="project", help="CLI for the project/repository.")

for subapp in MOUNT_SUBAPPS:
    project_app.command(subapp)
