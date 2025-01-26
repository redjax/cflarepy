from __future__ import annotations

from dynaconf import Dynaconf

CLOUDFLARE_SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="CF",
    settings_files=["settings.toml", ".secrets.toml"],
)
