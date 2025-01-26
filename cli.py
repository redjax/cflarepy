from loguru import logger as log

from project_cli import start_cli, cli_app
import setup, settings


if __name__ == "__main__":
    setup.setup_loguru_logging(log_level="ERROR", log_fmt="basic")
    start_cli(cli_app=cli_app)
