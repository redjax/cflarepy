from loguru import logger as log
import typing as t
from pathlib import Path
import ipaddress

import core_utils.path_utils
import settings, core_utils
from cfapi.controllers import CloudflareController
from project_cli.constants import IP_BLOCKS_FILE, COUNTRY_BLOCKS_FILE, UA_BLOCKS_FILE
from .methods import sort_ip_addresses, sort_country_codes, sort_ua_strings, dedupe_country_codes

from cyclopts import App, Group, Parameter

cleanup_app = App(name="cleanup", help="CLI for cleanup operations.")


@cleanup_app.command(name="sort-waf-filters")
def sort_waf_filters(
    overwrite: t.Annotated[bool, Parameter(
        name="overwrite",
        help="Overwrite existing files after sorting."
    )] = False
):
    """Sort WAF filter input files (alphabetically, by IP address, etc).
    
    Params:
        overwrite (bool): Whether to overwrite existing files after sorting.
    """
    print(f"Sorting IP addresses in file '{IP_BLOCKS_FILE}'")
    try:
        sort_ip_addresses(file_path=IP_BLOCKS_FILE, overwrite=overwrite)
    except Exception as exc:
        log.error(f"Error sorting IP addresses in file '{IP_BLOCKS_FILE}': {exc}")
        print(f"Failed sorting file '{IP_BLOCKS_FILE}'")
    
    print(f"Sorting country codes in file '{COUNTRY_BLOCKS_FILE}'")
    try:
        sort_country_codes(file_path=COUNTRY_BLOCKS_FILE, overwrite=overwrite)
    except Exception as exc:
        log.error(f"Error sorting country codes in file '{COUNTRY_BLOCKS_FILE}': {exc}")
        print(f"Failed sorting file '{COUNTRY_BLOCKS_FILE}'")
    
    try:
        print(f"Sorting UA strings in file  '{UA_BLOCKS_FILE}'")
        sort_ua_strings(file_path=UA_BLOCKS_FILE, overwrite=overwrite)
    except Exception as exc:
        log.error(f"Error sorting UA strings in file '{UA_BLOCKS_FILE}': {exc}")
        print(f"Failed sorting file '{UA_BLOCKS_FILE}'")


@cleanup_app.command(name="dedupe-waf-filters")
def dedupe_waf_filter_files(
    overwrite: t.Annotated[bool, Parameter(
        name="overwrite",
        help="Overwrite existing files after sorting."
    )] = False
):
    try:
        dedupe_country_codes(file_path=COUNTRY_BLOCKS_FILE, overwrite=overwrite)
    except Exception as exc:
        msg = f"({type(exc)}) Error deduplicating country codes in file '{COUNTRY_BLOCKS_FILE}'. Details: {exc}"
        log.error(msg)
        print(f"Failed deduplicating country codes in file '{COUNTRY_BLOCKS_FILE}'")
    print(f"Finished deduplicating country codes in file '{COUNTRY_BLOCKS_FILE}'")

    # print(f"Sorting IP addresses in file '{IP_BLOCKS_FILE}'")
    # try:
    #     sort_ip_addresses(file_path=IP_BLOCKS_FILE, overwrite=overwrite)
    # except Exception as exc:
    #     log.error(f"Error sorting IP addresses in file '{IP_BLOCKS_FILE}': {exc}")
    #     print(f"Failed sorting file '{IP_BLOCKS_FILE}'")
    
    # print(f"Sorting country codes in file '{COUNTRY_BLOCKS_FILE}'")
    # try:
    #     sort_country_codes(file_path=COUNTRY_BLOCKS_FILE, overwrite=overwrite)
    # except Exception as exc:
    #     log.error(f"Error sorting country codes in file '{COUNTRY_BLOCKS_FILE}': {exc}")
    #     print(f"Failed sorting file '{COUNTRY_BLOCKS_FILE}'")
    
    # try:
    #     print(f"Sorting UA strings in file  '{UA_BLOCKS_FILE}'")
    #     sort_ua_strings(file_path=UA_BLOCKS_FILE, overwrite=overwrite)
    # except Exception as exc:
    #     log.error(f"Error sorting UA strings in file '{UA_BLOCKS_FILE}': {exc}")
    #     print(f"Failed sorting file '{UA_BLOCKS_FILE}'")
