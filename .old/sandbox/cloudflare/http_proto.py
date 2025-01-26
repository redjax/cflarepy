from __future__ import annotations

import json
import typing as t

from cflarepy.libs import http_lib, settings, setup

import httpx
from loguru import logger as log
import pandas as pd

def list_zones(http_controller: http_lib.HttpxController):
    with http_controller as http_ctl:
        req = http_lib.build_request(url="https://api.cloudflare.com/client/v4/zones", headers=http_controller.headers)
        
        log.info("Requesting Cloudflare account zones")
        try:
            zones_res = http_ctl.send_request(request=req)
            zones_res.raise_for_status()
        except Exception as exc:
            msg = f"({type(exc)}) Error getting Cloudflare account zones. Details: {exc}"
            log.error(msg)
            
            raise exc
        
        if not zones_res.status_code == 200:
            log.warning(f"Non-200 status code requesting all zones: [{zones_res.status_code}: {zones_res.reason_phrase}]: {zones_res.text}")
            return
        
        log.success(f"[{zones_res.status_code}: {zones_res.reason_phrase}]")
        
        log.debug(f"Request zones response: {zones_res}")
        res_dict = http_lib.decode_response(response=zones_res)
        log.debug(f"Response ({type(res_dict)}): {res_dict}")
        res = res_dict["result"]
        
        return res
    

def get_zone_waf_filters(http_controller: http_lib.HttpxController, zone_id: str):
    with http_controller as http_ctl:
        req = http_lib.build_request(url=f"https://api.cloudflare.com/client/v4/zones/{zone_id}/filters", headers=http_controller.headers)
        
        log.info("Requesting Cloudflare zone WAF filters")
        try:
            zone_filters_res = http_ctl.send_request(request=req)
            log.success(f"Cloudflare zone WAF filters requested. [{zone_filters_res.status_code}: {zone_filters_res.reason_phrase}]")
        except Exception as exc:
            msg = f"({type(exc)}) Error getting Cloudflare zone WAF filters. Details: {exc}"
            log.error(msg)
            
            raise exc
        
        if not zone_filters_res.status_code == 200:
            log.warning(f"Non-200 status code requesting zone WAF filters: [{zone_filters_res.status_code}: {zone_filters_res.reason_phrase}]: {zone_filters_res.text}")
            return
        
        log.debug(f"Request zone WAF filters response: {zone_filters_res} [{zone_filters_res.status_code if zone_filters_res else '<error>'}: {zone_filters_res.reason_phrase if zone_filters_res else '<error>'}]: {zone_filters_res.reason_phrase if zone_filters_res else '<error>'}")
        res_dict = http_lib.decode_response(response=zone_filters_res)
        log.debug(f"Response ({type(res_dict)}): {res_dict}")
        res = res_dict["result"]
        
        return res
    
def main():
    api_token = settings.CLOUDFLARE_SETTINGS.get("CF_API_TOKEN")
    api_email = settings.CLOUDFLARE_SETTINGS.get("CF_API_EMAIL")
    api_key = settings.CLOUDFLARE_SETTINGS.get("CF_API_KEY")
    
    # if not api_token:
    #     if not api_email:
    #         raise ValueError("Missing a Cloudflare account email")
    #     if not api_key:
    #         raise ValueError("Missing a Cloudflare account API key")
        
    #     headers = {"X-Auth-Email": api_email, "X-Auth-Key": api_key}
    # else:
    #     headers =  {"X-Auth-Token": settings.CLOUDFLARE_SETTINGS.get("CF_API_TOKEN")}
    
    # headers = {"X-Auth-Email": api_email, "X-Auth-Key": api_token}
    headers = {"Authorization": f"Bearer {api_token}"}
    log.debug(f"HTTP headers: {headers}")
    
    http_controller = http_lib.HttpxController(headers=headers)
    
    ## Get zones
    zones = list_zones(http_controller)
    log.debug(f"Zones ([{len(zones)}] {type(zones)})")
    
    zones_json = json.dumps(zones, indent=4, sort_keys=True, default=str)
    log.debug(f"Zones JSON: {zones_json}")
    
    with open("./sandbox/cloudflare/zones.json", "w") as f:
        f.write(zones_json)
        
    zones_df = pd.DataFrame(zones)
    log.debug(f"Zones Dataframe:\n{zones_df}")
    
    zones_df.to_parquet("./sandbox/cloudflare/zones.parquet", engine="pyarrow")
    
    waf_filters: list[dict] = []
    
    for zone in zones:
        log.debug(f"Getting WAF filter rules for zone '{zone['name']}")
        filters = get_zone_waf_filters(http_controller=http_controller, zone_id=zone["id"])
        _res = {"zone": {"name": zone["name"], "id": zone["id"]}, "filters": filters}
        waf_filters.append(_res)
        
    log.info(f"Retrieved [{len(waf_filters)}] zone WAF filter(s)")
    
    waf_filters_json = json.dumps(waf_filters, indent=4, sort_keys=True, default=str)
    with open("./sandbox/cloudflare/waf_filters.json", "w") as f:
        f.write(waf_filters_json)

    

if __name__ == "__main__":
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"), colorize=True)
    
    main()
