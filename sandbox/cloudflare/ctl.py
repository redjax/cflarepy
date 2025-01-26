from __future__ import annotations

import json
import typing as t

from cfapi import CloudflareController
import http_lib, settings, setup
from domain import cloudflare as cf_domain

import httpx
from loguru import logger as log
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
    
    zones = cf_controller.get_zones()
    log.info(f"Loaded [{len(zones)}] zone(s)")
    
    zone_schemas = cf_domain.CloudflareZones(zones=zones)
    log.debug(f"Zones: {zone_schemas}")
    
    input("PAUSE")
    
    waf_filters = []
    
    for zone in zones:
        zone_waf_filters = cf_controller.get_zone_waf_filters(zone_id=zone["id"])
        filter_dict = {"zone": {"name": zone["name"], "id": zone["id"]}, "filters": zone_waf_filters}
        # log.debug(f"Filter dict: {filter_dict}")
        waf_filters.append(filter_dict)
    
    log.info(f"Retrieved [{len(waf_filters)}] WAF filter(s)")
    
    for waf_filter in waf_filters:
        log.debug(f"""[WAF Filter]
Zone: {waf_filter['zone']}

Filters:
{waf_filter['filters']}
""")
        
    with open("./sandbox/cloudflare/waf_filters.json", "w") as f:
        f.write(json.dumps(waf_filters, indent=4, sort_keys=True, default=str))

    
if __name__ == "__main__":
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"), colorize=True)
    
    main(email=settings.CLOUDFLARE_SETTINGS.get("CF_API_EMAIL"), api_key=settings.CLOUDFLARE_SETTINGS.get("CF_API_KEY"), api_token=settings.CLOUDFLARE_SETTINGS.get("CF_API_TOKEN"))
