from loguru import logger as log

from cflarepy.libs import settings
from cflarepy.controllers import CloudflareController

from cyclopts import App, Group, Parameter

cf_zones_app = App(name="zones", help="CLI for Cloudflare zones operations.")

@cf_zones_app.command(name="list")
def list_cf_zones():
    print(f"Test settings: {settings.CLOUDFLARE_SETTINGS.as_dict()}")
    api_token = settings.CLOUDFLARE_SETTINGS.get("CF_API_TOKEN")
    api_email = settings.CLOUDFLARE_SETTINGS.get("CF_API_EMAIL")
    api_key = settings.CLOUDFLARE_SETTINGS.get("CF_API_KEY")
    
    cf_controller = CloudflareController(account_email=api_email, api_key=api_key, api_token=api_token)
    
    zones = cf_controller.get_zones()
    
    print(f"Zones ([{len(zones)}] {type(zones)})")
