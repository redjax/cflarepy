from loguru import logger as log
import typing as t
from cflarepy.libs import setup
from cflarepy.libs import settings
from cflarepy.libs import http_lib
from cflarepy.controllers import CloudflareController

import json

import httpx
import pandas as pd


def main(email: str, api_key: str, api_token: str):
    cf_controller: CloudflareController = CloudflareController(account_email=email, api_key=api_key, api_token=api_token)
    log.debug(f"Cloudflare controller: {cf_controller}")
    
    accounts = cf_controller.get_accounts()
    log.info(f"Loaded [{len(accounts)}] account(s)")
    
    if len(accounts) == 1:
        account: dict = accounts[0]
        log.info(f"Account: {account}")
        account_id: str = account["id"]
        log.info(f"Account ID: {account_id}")
    else:
        raise NotImplementedError("Multiple accounts not supported yet")
    
    
if __name__ == "__main__":
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"), colorize=True)
    
    main(email=settings.CLOUDFLARE_SETTINGS.get("CF_API_EMAIL"), api_key=settings.CLOUDFLARE_SETTINGS.get("CF_API_KEY"), api_token=settings.CLOUDFLARE_SETTINGS.get("CF_API_TOKEN"))
