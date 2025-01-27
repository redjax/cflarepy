from loguru import logger as log
import typing as t
from pathlib import Path
import core_utils
import ipaddress


def sort_country_codes(
    file_path: t.Union[str, Path],
    output_path: t.Union[str, Path] | None = None,
    overwrite: bool = False,
) -> bool:
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

    file_path = (
        Path(file_path).expanduser().resolve()
        if "~" in file_path
        else Path(file_path).resolve()
    )
    log.debug(f"File path: {file_path}")

    # Determine output path
    if not output_path:
        if overwrite:
            log.warning(f"No output_path detected. Overwriting file '{file_path}'")
            output_path = file_path
        else:
            log.warning(
                f"No output_path detected. Did not sort country codes in file '{file_path}'"
            )
            return False
    else:
        output_path = Path(output_path).expanduser().resolve()

    ## Read and sort the country codes
    country_codes = core_utils.path_utils.read_file(file_path=file_path)

    log.info("Sorting country codes...")
    try:
        sorted_codes = sorted(country_codes)
    except Exception as exc:
        msg = f"({type(exc).__name__}) Error sorting country codes: {exc}"
        log.error(msg)
        raise exc

    ## Write sorted codes to the output file
    log.info(f"Writing sorted country codes to file '{output_path}'")
    try:
        with open(output_path, "w") as file:
            file.write("\n".join(sorted_codes))
    except Exception as exc:
        msg = f"({type(exc).__name__}) Unhandled exception writing sorted country codes to file '{output_path}': {exc}"
        log.error(msg)
        raise exc

    log.info(f"Successfully wrote sorted country codes to '{output_path}'")
    return True


def sort_ip_addresses(
    file_path: t.Union[str, Path],
    output_path: t.Union[str, Path] | None = None,
    overwrite: bool = False,
) -> bool:
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
            log.warning(
                f"No output_path detected. Did not sort IP addresses in file '{file_path}'"
            )
            return False
    else:
        output_path = Path(output_path).expanduser().resolve()

    log.info(f"Reading file '{file_path}'")
    ip_addresses = core_utils.path_utils.read_file(file_path=file_path)

    log.info("Sorting IP addresses...")
    try:
        sorted_ips = sorted(ip_addresses, key=lambda ip: ipaddress.ip_address(ip))
    except Exception as exc:
        msg = f"({type(exc).__name__}) Error sorting IP addresses: {exc}"
        log.error(msg)
        raise exc

    log.info(f"Writing sorted IP addresses to file '{output_path}'")
    try:
        with open(output_path, "w") as file:
            file.write("\n".join(sorted_ips))
    except Exception as exc:
        msg = f"({type(exc).__name__}) Unhandled exception writing sorted IP addresses to file '{output_path}': {exc}"
        log.error(msg)
        raise exc

    log.info(f"Successfully wrote sorted IP addresses to '{output_path}'")
    return True


def sort_ua_strings(
    file_path: t.Union[str, Path],
    output_path: t.Union[str, Path] | None = None,
    overwrite: bool = False,
) -> bool:
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
            log.warning(
                f"No output_path detected. Did not sort User Agent strings in file '{file_path}'"
            )
            return False
    else:
        output_path = Path(output_path).expanduser().resolve()

    log.info(f"Reading file '{file_path}'")
    regex_strings = core_utils.path_utils.read_file(file_path=file_path)

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
        with open(output_path, "w") as file:
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


def deduplicate_strings(str_list: list[str]) -> list[str]:
    """Removes duplicate strings in a list.

    Params:
        str_list (list[str]): List of strings to deduplicate.

    Returns:
        (list[str]): List of unique country codes.

    """
    seen = set()
    result: list[str] = []

    for code in str_list:
        if code not in seen:
            result.append(code)
            seen.add(code)

    return result


def dedupe_country_codes(file_path: str, overwrite: bool = False):
    country_codes = core_utils.path_utils.read_file(file_path=file_path)
    log.debug(f"Loaded country codes: {country_codes}")
    print(f"Country codes from file: {country_codes}")

    log.info(f"Deduplicating country codes in file '{file_path}'")
    try:
        deduped_countries = deduplicate_strings(str_list=country_codes)
    except Exception as exc:
        log.error(f"Error deduplicating country codes in file '{file_path}': {exc}")
        print(f"Failed deduplicating file '{file_path}'")

        raise

    if core_utils.path_utils.path_exists(p=file_path):
        if not overwrite:
            log.warning(
                f"Path exists: {file_path}. Overwrite=False, deduplicated list will not be saved."
            )
            return

    log.info(f"Saving deduplicated country codes to file: '{file_path}'")
    try:
        with open(file_path, "w") as f:
            f.write("\n".join(deduped_countries))
    except PermissionError:
        log.error(f"Permission denied saving file '{file_path}'.")
        print(f"Failed saving file '{file_path}'")

        raise
    except Exception as exc:
        log.error(
            f"Error saving deduplicated country codes to file '{file_path}': {exc}"
        )
        print(f"Failed saving file '{file_path}'")

        raise
