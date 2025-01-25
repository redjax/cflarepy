from loguru import logger as log
from cflarepy.libs import setup, settings, http_lib

def main():
    log.info("cflarepy startup")


if __name__ == "__main__":
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"))

    main()
