from loguru import logger as log

from cflarepy.libs import settings
from cflarepy.controllers import CloudflareController

from cyclopts import App, Group, Parameter


cf_zones_app = App(name="zones", help="CLI for Cloudflare zones operations.")

@cf_zones_app.command(name="list")
def list_cf_zones():
    api_token = settings.CLOUDFLARE_SETTINGS.get("CF_API_TOKEN")
    api_email = settings.CLOUDFLARE_SETTINGS.get("CF_API_EMAIL")
    api_key = settings.CLOUDFLARE_SETTINGS.get("CF_API_KEY")
    
    if not api_token:
        if not api_email:
            raise ValueError("Missing a Cloudflare account email")
        if not api_key:
            raise ValueError("Missing a Cloudflare account API key")
        
        headers = {"X-Auth-Email": api_email, "X-Auth-Key": api_key}
    else:
        headers =  {"X-Auth-Token": settings.CLOUDFLARE_SETTINGS.get("CF_API_TOKEN")}
    
    cf_client = CloudflareController(headers=headers)
    
    zones = cf_client.get_zones()
    
    print(f"Zones ([{len(zones)}] {type(zones)})")
