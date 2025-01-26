from loguru import logger as log
import typing as t
from cflarepy.libs import setup
from cflarepy.libs import settings
from cflarepy.libs import http_lib

import json

import httpx
import pandas as pd


def list_zones(http_controller: http_lib.HttpxController):
    with http_controller as http_ctl:
        req = http_lib.build_request(url="https://api.cloudflare.com/client/v4/zones")
        
        log.info("Requesting Cloudflare account zones")
        try:
            zones_res = http_ctl.send_request(request=req)
            log.success(f"Cloudflare zones requested. [{zones_res.status_code}: {zones_res.reason_phrase}]")
        except Exception as exc:
            msg = f"({type(exc)}) Error getting Cloudflare account zones. Details: {exc}"
            log.error(msg)
            
            raise exc
        
        if not zones_res.status_code == 200:
            log.warning(f"Non-200 status code requesting all zones: [{zones_res.status_code}: {zones_res.reason_phrase}]: {zones_res.text}")
            return
        
        log.debug(f"Request zones response: {zones_res}")
        res_dict = http_lib.decode_response(response=zones_res)
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
    
    for zone in zones:
        log.debug(f"Zone: {zone}\n")
    
    zones_df = pd.DataFrame(zones)
    log.debug(f"Zones Dataframe:\n{zones_df}")

    

if __name__ == "__main__":
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"), colorize=True)
    
    main()
