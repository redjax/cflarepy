from __future__ import annotations

from cflarepy.libs import http_lib, settings, setup

from loguru import logger as log

def main():
    log.info("cflarepy startup")


if __name__ == "__main__":
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"))

    main()
