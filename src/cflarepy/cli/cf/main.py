from loguru import logger as log

from cflarepy.libs import settings
from cflarepy.controllers import CloudflareController

from cyclopts import App, Group, Parameter
from .zones import cf_zones_app


cf_app = App(name="cloudflare", help="CLI for Cloudflare operations.")

cf_app.command(cf_zones_app)
