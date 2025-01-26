from loguru import logger as log

from cflarepy.cli import start_cli, cli_app


if __name__ == "__main__":
    start_cli(cli_app=cli_app)
