from loguru import logger as log

from cflarepy.libs import setup
from cflarepy.libs import settings

from cloudflare import Cloudflare
from cloudflare.types.zones import Zone
from cloudflare.types import rules, rulesets
from cloudflare import pagination

import json


def get_zones(cf_client: Cloudflare) -> list[Zone]:
    zones = []

    log.info("Getting Cloudflare zones")
    try:
        for zone in cf_client.zones.list():
            zones.append(zone)
    except Exception as exc:
        msg = f"({type(exc)}) Error getting Cloudflare zones. Details: {exc}"
        log.error(msg)
        
        raise exc
        
    log.debug(f"Zones: {zones}")
    
    return zones


def iter_zone_waf_rules(cf_client: Cloudflare, zones: list[Zone]):
    rules_lst = []
    rulesets_lst: list[pagination.SyncSinglePage[rulesets.RulesetListResponse]] = []

    try:
        for zone in zones:
            zone_name = zone.name
            zone_id = zone.id
            log.debug(f"Zone: [{zone_id}] - {zone_name}", zone_name, zone_id)
            
            # _zone = cf_client.zones.get(zone_id=zone_id)
            _rulesets: pagination.SyncSinglePage[rulesets.RulesetListResponse] = cf_client.rulesets.list(zone_id=zone_id)
            
            rulesets_lst.append(_rulesets)
            
            for _rule in _rulesets:
                print(f"Rule ({type(_rule)}): {_rule}")
                rules_lst.append(_rule)
            
            ## Retrieve WAF rulesets for zone
    except Exception as exc:
        msg = f"({type(exc)}) Error getting Cloudflare zone WAF rulesets. Details: {exc}"
        log.error(msg)
        
        raise exc
        
def main(api_email: str = settings.CLOUDFLARE_SETTINGS.get("CF_API_EMAIL"), api_key: str = settings.CLOUDFLARE_SETTINGS.get("CF_API_TOKEN"), api_token: str = settings.CLOUDFLARE_SETTINGS.get("CF_API_TOKEN")):
    if not api_email:
        raise ValueError("Missing a Cloudflare account email")
    if not api_token:
        raise ValueError("Missing a Cloudflare account API key")

    client = Cloudflare(
        api_token=api_token,
    )
    
    zones: list[Zone] = get_zones(cf_client=client)
    log.debug(f"Retrieved [{len(zones)}] zone(s)")
    
    # print(f"Zone 1: {zones[0]}")
    
    zone_dicts = [z.model_dump() for z in zones]
    
    log.debug(f"Zone 1: [{zone_dicts[0]}]")
    
    log.info(f"Saving Cloudflare zones to ./sandbox/cloudflare/zones.json")
    with open("./sandbox/cloudflare/zones.json", "w") as f:
        zone_dump = json.dumps(zone_dicts[0], indent=4, sort_keys=True, default=str)
        f.write(zone_dump)
        
    iter_zone_waf_rules(cf_client=client, zones=zones)
    

if __name__ == "__main__":
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"))
    main()
