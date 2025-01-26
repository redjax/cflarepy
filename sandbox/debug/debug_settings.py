from __future__ import annotations

import time

import settings

## When True, passwords & other secrets will be printed to the command line.
PRINT_SENSITIVE: bool = True


def debug_log_level():
    print(f"""
[Log level]
{settings.LOGGING_SETTINGS.get('LOG_LEVEL')}""")


def debug_timezone():
    print(f"""
[Timezone]
{settings.APP_SETTINGS.get('TZ')}""")


def debug_db_config(print_password: bool = False):
    print(f"""
[Database config]
Type: {settings.DB_SETTINGS.get('DB_TYPE')}
Host: {settings.DB_SETTINGS.get('DB_HOST')}
Port: {settings.DB_SETTINGS.get('DB_PORT')}
Username: {settings.DB_SETTINGS.get('DB_USERNAME')}
Password: {settings.DB_SETTINGS.get('DB_PASSWORD')}
Database: {settings.DB_SETTINGS.get('DB_DATABASE') if print_password else "[REDACTED]"}""")
    
    
def debug_cloudflare_config(print_password: bool = False):
    print(f"""
[Cloudflare config]
Email: {settings.CLOUDFLARE_SETTINGS.get('CF_API_EMAIL')}
API Key: {settings.CLOUDFLARE_SETTINGS.get('CF_API_TOKEN') if print_password else "[REDACTED]"}""")


def main(print_sensitive: bool = False):
    if print_sensitive:
        print(f"[WARNING] print_sensitive=True, secrets will be printed to the command line.")
        time.sleep(1)

    debug_timezone()
    debug_log_level()
    debug_db_config(print_password=print_sensitive)
    debug_cloudflare_config(print_password=print_sensitive)


if __name__ == "__main__":
    main(print_sensitive=True)
