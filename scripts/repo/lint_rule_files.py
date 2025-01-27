from loguru import logger as log

import ipaddress
import typing as t

from pathlib import Path

import settings, setup

WAF_FILTER_RULES_DIR: str = "./.data/cf_waf_filter_rules"

IP_BLOCKS_TXT = f"{WAF_FILTER_RULES_DIR}/block_ips.txt"
COUNTRY_BLOCKS_TXT = f"{WAF_FILTER_RULES_DIR}/countries.txt"
UA_BLOCKS_TXT = f"{WAF_FILTER_RULES_DIR}/ua_strings.txt"


def path_exists(p: t.Union[str, Path]) -> bool:
    """Check if a path exists.
    
    Params:
        p (str | Path): Path to check.
    
    Returns:
        (bool): True if path exists, False otherwise.
    
    """
    p: Path = Path(str(p)).expanduser() if "~" in p else Path(str(p))
    
    return p.exists()


def read_file(file_path: t.Union[str, Path], mode: str = "r") -> t.Any:
    """Reads a file and returns its contents as a list of lines.
    
    Params:
        file_path (str | Path): Path to the file to read.
        mode (str): Mode to open the file in. Options: ['r', 'r+', 'rb', 'rb+']
    
    Returns:
        (list): List of lines in the file.

    """
    if mode not in ["r", "r+", "rb", "rb+"]:
        raise ValueError(f"Invalid mode: '{mode}'. Must be one of: ['r', 'r+', 'rb', 'rb+']")

    file_path = Path(str(file_path)).expanduser().resolve() if "~" in str(file_path) else Path(str(file_path)).resolve()
    
    log.info(f"Reading file '{file_path}'")
    try:
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()
    except PermissionError:
        log.error(f"Permission denied reading file '{file_path}'.")
        raise
    except FileNotFoundError:
        log.error(f"File '{file_path}' not found.")
        raise
    except Exception as exc:
        msg = f"({type(exc).__name__}) Unhandled exception reading file '{file_path}': {exc}"
        log.error(msg)
        raise
    
    return lines


def sort_country_codes(file_path: t.Union[str, Path], output_path: t.Union[str, Path] | None = None, overwrite: bool = False) -> bool:
    """Sorts country codes in a text file alphabetically and writes the output to a new file.
    
    Params:
        file_path (str | Path): Path to the file to read.
        output_path (str | Path | None): Path to the file to write the sorted country codes to. If no output_path is used, and overwrite=True,
            file will be overwritten in-place.
        overwrite (bool): Whether to overwrite the output file if it already exists. Defaults to False.
    
    Returns:
        (bool): True if the country codes were successfully sorted and written to the output file, False otherwise.
    
    """
    if not file_path:
        raise ValueError("Missing file path to read")

    file_path = Path(file_path).expanduser().resolve() if "~" in file_path else Path(file_path).resolve()
    log.debug(f"File path: {file_path}")

    # Determine output path
    if not output_path:
        if overwrite:
            log.warning(f"No output_path detected. Overwriting file '{file_path}'")
            output_path = file_path
        else:
            log.warning(f"No output_path detected. Did not sort country codes in file '{file_path}'")
            return False
    else:
        output_path = Path(output_path).expanduser().resolve()

    # Read and sort the country codes
    country_codes = read_file(file_path=file_path)

    log.info("Sorting country codes...")
    try:
        sorted_codes = sorted(country_codes)
    except Exception as exc:
        msg = f"({type(exc).__name__}) Error sorting country codes: {exc}"
        log.error(msg)
        raise exc

    # Write sorted codes to the output file
    log.info(f"Writing sorted country codes to file '{output_path}'")
    try:
        with open(output_path, 'w') as file:
            file.write("\n".join(sorted_codes))
    except Exception as exc:
        msg = f"({type(exc).__name__}) Unhandled exception writing sorted country codes to file '{output_path}': {exc}"
        log.error(msg)
        raise exc

    log.info(f"Successfully wrote sorted country codes to '{output_path}'")
    return True


def sort_ip_addresses(file_path: t.Union[str, Path], output_path: t.Union[str, Path] | None = None, overwrite: bool = False) -> bool:
    """Sorts IP addresses in a text file numerically and writes the output to a new file.
    
    Params:
        file_path (str | Path): Path to the file to read.
        output_path (str | Path | None): Path to the file to write the sorted IP addresses to. If no output_path is used, and overwrite=True,
            file will be overwritten in-place.
        overwrite (bool): Whether to overwrite the output file if it already exists. Defaults to False.
    
    Returns:
        (bool): True if the IP addresses were successfully sorted and written to the output file, False otherwise.

    """
    if not file_path:
        raise ValueError("Missing file path to read")

    file_path = Path(file_path).expanduser().resolve()

    if not file_path.exists():
        msg = f"File '{file_path}' does not exist"
        log.error(msg)
        raise FileNotFoundError(msg)

    if not output_path:
        if overwrite:
            log.warning(f"No output_path detected. Overwriting file '{file_path}'")
            output_path = file_path
        else:
            log.warning(f"No output_path detected. Did not sort IP addresses in file '{file_path}'")
            return False
    else:
        output_path = Path(output_path).expanduser().resolve()

    log.info(f"Reading file '{file_path}'")
    ip_addresses = read_file(file_path=file_path)

    log.info("Sorting IP addresses...")
    try:
        sorted_ips = sorted(ip_addresses, key=lambda ip: ipaddress.ip_address(ip))
    except Exception as exc:
        msg = f"({type(exc).__name__}) Error sorting IP addresses: {exc}"
        log.error(msg)
        raise exc

    log.info(f"Writing sorted IP addresses to file '{output_path}'")
    try:
        with open(output_path, 'w') as file:
            file.write("\n".join(sorted_ips))
    except Exception as exc:
        msg = f"({type(exc).__name__}) Unhandled exception writing sorted IP addresses to file '{output_path}': {exc}"
        log.error(msg)
        raise exc

    log.info(f"Successfully wrote sorted IP addresses to '{output_path}'")
    return True


def sort_ua_strings(file_path: t.Union[str, Path], output_path: t.Union[str, Path] | None = None, overwrite: bool = False) -> bool:
    """Sorts User Agent regex strings in a text file alphabetically (ignoring wildcards) & writes the output to a new file while preserving the original wildcards.
    
    Params:
        file_path (str | Path): Path to the file to read.
        output_path (str | Path | None): Path to the file to write the sorted User Agent strings to. If no output_path is used, and overwrite=True,
            file will be overwritten in-place.
        overwrite (bool): Whether to overwrite the output file if it already exists. Defaults to False.
    
    Returns:
        (bool): True if the User Agent strings were successfully sorted and written to the output file, False otherwise.

    """
    if not file_path:
        raise ValueError("Missing file path to read")

    file_path = Path(file_path).expanduser().resolve()

    if not file_path.exists():
        msg = f"File '{file_path}' does not exist"
        log.error(msg)
        raise FileNotFoundError(msg)

    if not output_path:
        if overwrite:
            log.warning(f"No output_path detected. Overwriting file '{file_path}'")
            output_path = file_path
        else:
            log.warning(f"No output_path detected. Did not sort User Agent strings in file '{file_path}'")
            return False
    else:
        output_path = Path(output_path).expanduser().resolve()

    log.info(f"Reading file '{file_path}'")
    regex_strings = read_file(file_path=file_path)

    log.info("Sorting User Agent strings...")
    try:
        ## Sort based on the strings ignoring the wildcards
        sorted_regex = sorted(regex_strings, key=lambda s: s.replace("*", ""))
    except Exception as exc:
        msg = f"({type(exc).__name__}) Error sorting User Agent strings: {exc}"
        log.error(msg)
        raise exc

    log.info(f"Writing sorted User Agent strings to file '{output_path}'")
    try:
        with open(output_path, 'w') as file:
            file.write("\n".join(sorted_regex))
    except PermissionError:
        log.error(f"Permission denied reading file '{file_path}'.")
        raise
    except FileNotFoundError:
        log.error(f"File '{file_path}' not found.")
        raise
    except Exception as exc:
        msg = f"({type(exc).__name__}) Unhandled exception reading file '{file_path}': {exc}"
        log.error(msg)
        raise

    log.info(f"Successfully wrote sorted User Agent strings to '{output_path}'")
    return True
 

def main(country_blocks_file: t.Union[str, Path], ip_blocks_file: t.Union[str, Path], ua_blocks_file: t.Union[str, Path]):
    if country_blocks_file:
        country_blocks_file = str(country_blocks_file)
    if ip_blocks_file:
        ip_blocks_file = str(ip_blocks_file)
    if ua_blocks_file:
        ua_blocks_file = str(ua_blocks_file)

    if path_exists(country_blocks_file):
        log.info(f"Sorting country codes in file '{country_blocks_file}'")
        country_code_success = sort_country_codes(file_path=country_blocks_file, overwrite=True)
        log.info(f"Sort country codes success: {country_code_success}")
    else:
        raise FileNotFoundError(f"Could not find country code blocklist file at path: {country_blocks_file}")
    
    if path_exists(ip_blocks_file):
        log.info(f"Sorting IP addresses in file '{ip_blocks_file}'")
        sort_ip_addresses(file_path=ip_blocks_file, overwrite=True)
        log.info(f"Sort IP addresses success")

    if path_exists(ua_blocks_file):
        log.info(f"Sorting User Agent strings in file '{ua_blocks_file}'")
        sort_ua_strings(file_path=ua_blocks_file, overwrite=True)
        log.info(f"Sort User Agent strings success")


if __name__ == "__main__":
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.LOG_LEVEL or "INFO", colorize=True)

    log.debug(f"IP blocks file: {IP_BLOCKS_TXT} | Exists: {path_exists(p=IP_BLOCKS_TXT)}")
    log.debug(f"Country blocks file: {COUNTRY_BLOCKS_TXT} | Exists: {path_exists(p=COUNTRY_BLOCKS_TXT)}")
    log.debug(f"User agent blocks file: {UA_BLOCKS_TXT} | Exists: {path_exists(p=UA_BLOCKS_TXT)}")
    
    main(country_blocks_file=COUNTRY_BLOCKS_TXT, ip_blocks_file=IP_BLOCKS_TXT, ua_blocks_file=UA_BLOCKS_TXT)
    