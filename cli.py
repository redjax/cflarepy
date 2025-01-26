from loguru import logger as log

from cflarepy.cli import start_cli, cli_app
from cflarepy.libs import setup, settings


if __name__ == "__main__":
    setup.setup_loguru_logging(log_level="ERROR", log_fmt="basic")
    start_cli(cli_app=cli_app)
