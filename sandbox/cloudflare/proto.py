from loguru import logger as log

from cflarepy.libs import setup
from cflarepy.libs import settings

from cloudflare import Cloudflare



def get_zones(cf_client: Cloudflare):
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

def main(api_email: str = settings.CLOUDFLARE_SETTINGS.get("CF_API_EMAIL"), api_key: str = settings.CLOUDFLARE_SETTINGS.get("CF_API_KEY")):
    if not api_email:
        raise ValueError("Missing a Cloudflare account email")
    if not api_key:
        raise ValueError("Missing a Cloudflare account API key")

    client = Cloudflare(
        api_token=api_key,
    )
    
    zones = get_zones(cf_client=client)
    log.debug(f"Retrieved [{len(zones)}] zone(s)")
    

if __name__ == "__main__":
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"))
    main()
