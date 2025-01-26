from loguru import logger as log

import settings
from cfapi.controllers import CloudflareController

from cyclopts import App, Group, Parameter
import pandas as pd

cf_zones_app = App(name="zones", help="CLI for Cloudflare zones operations.")

@cf_zones_app.command(name="list")
def list_cf_zones(email: str | None = None, api_key: str | None = None, api_token: str | None = None):
    if not api_token or api_token == "":
        api_token = settings.CLOUDFLARE_SETTINGS.get("CF_API_TOKEN")
    if not email or email == "":
        api_email = settings.CLOUDFLARE_SETTINGS.get("CF_API_EMAIL")
    if not api_key or api_key == "":
        api_key = settings.CLOUDFLARE_SETTINGS.get("CF_API_KEY")
    
    cf_controller = CloudflareController(account_email=api_email, api_key=api_key, api_token=api_token)
    
    try:
        zones = cf_controller.get_zones()
        log.debug(f"Zones ([{len(zones)}] {type(zones)})")
    except Exception as exc:
        msg = f"({type(exc)}) Error getting Cloudflare zones. Details: {exc}"
        log.error(msg)
        
        return
    
    zones_df = pd.DataFrame(zones)
    print(f"Zones:\n{zones_df}")
