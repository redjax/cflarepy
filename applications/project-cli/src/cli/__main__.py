from __future__ import annotations

from cyclopts import App
from loguru import logger as log
from cli.main import app as cli_app, start_cli

    
if __name__ == "__main__":
    start_cli(cli_app=cli_app)
