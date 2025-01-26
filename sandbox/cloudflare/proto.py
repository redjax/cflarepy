from __future__ import annotations

import json
import typing as t

from cflarepy.libs import settings, setup

from cloudflare import Cloudflare, pagination
from cloudflare.types import rules, rulesets
from cloudflare.types.rulesets import RulesetListResponse
from cloudflare.types.zones import Zone
from loguru import logger as log

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
    rules_lst: list[RulesetListResponse] = []
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
                # log.debug(f"Rule '{_rule.name}' ({type(_rule)}): {_rule}")
                rules_lst.append(_rule)
            
            ## Retrieve WAF rulesets for zone
    except Exception as exc:
        msg = f"({type(exc)}) Error getting Cloudflare zone WAF rulesets. Details: {exc}"
        log.error(msg)
        
        raise exc
    
    
def iter_zone_custom_waf_rules(cf_client: Cloudflare, zones: list[Zone]):
    zone_rulesets: list[dict[str, t.Union[str, RulesetListResponse]]] = []
    zone_rules: list = []

    for zone in zones:
        log.info(f"List custom WAF rules for zone: {zone.name}")
        
        rulesets: RulesetListResponse = cf_client.rulesets.list(zone_id=zone.id)
        _zonerules_dict = {"zone": zone.name, "zone_id": zone.id, "rulesets": rulesets} or None
        zone_rulesets.append(_zonerules_dict)
        
        for zone_ruleset in zone_rulesets:
            log.debug(f"Zone {zone.name} ruleset: {zone_ruleset.items()}") if zone_rulesets else None


def iter_zone_waf_packages(cf_client: Cloudflare, zones: list[Zone]):
    waf_pkgs = []
    for zone in zones:
        try:
            waf_packages = cf_client.firewall.waf.packages.list(zone_id=zone.id)
        except Exception as exc:
            msg = f"({type(exc)}) Error getting Cloudflare zone WAF packages. Details: {exc}"
            log.error(msg)
            
            continue
        waf_pkgs.append({"zone": {"name": zone.name, "id": zone.id}, "waf_packages": waf_packages})
        
        for pkg in waf_packages:
            log.debug(f"WAF package: {pkg}")
        

def main(api_email: str = settings.CLOUDFLARE_SETTINGS.get("API_EMAIL"), api_key: str = settings.CLOUDFLARE_SETTINGS.get("API_KEY"), api_token: str = settings.CLOUDFLARE_SETTINGS.get("API_TOKEN")):
    if not api_token:
        if not api_email:
            raise ValueError("Missing a Cloudflare account email")
        if not api_key:
            raise ValueError("Missing a Cloudflare account API key")
        
        client = Cloudflare(api_email=api_email, api_key=api_key)
    else:
        client = Cloudflare(
            api_token=api_token,
        )
    
    zones: list[Zone] = get_zones(cf_client=client)
    log.debug(f"Retrieved [{len(zones)}] zone(s)")
    
    zone_dicts = [z.model_dump() for z in zones]
    
    # log.debug(f"Zone 1: [{zone_dicts[0]}]")
    
    log.info(f"Saving Cloudflare zones to ./sandbox/cloudflare/zones.json")
    with open("./sandbox/cloudflare/zones.json", "w") as f:
        zone_dump = json.dumps(zone_dicts[0], indent=4, sort_keys=True, default=str)
        f.write(zone_dump)
        
    # iter_zone_waf_rules(cf_client=client, zones=zones)
    # iter_zone_custom_waf_rules(cf_client=client, zones=zones)
    iter_zone_waf_packages(cf_client=client, zones=zones)
    

if __name__ == "__main__":
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"))
    log.debug(f"Cloudflare settings: {settings.CLOUDFLARE_SETTINGS.as_dict()}")
    main()
