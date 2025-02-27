"""Bugreport extractor"""

import glob
import gzip
import os
from re import Match, Pattern, compile, search  # pylint: disable =W0622
from typing import Any, List, Union
from zipfile import ZipFile

from InquirerPy import inquirer
from prettytable import PrettyTable
from rich.console import Console

console = Console()

HOME: str = os.path.expanduser(path="~")
DOWNLOADS: str = os.path.join(HOME, "Downloads")
BUGREPORT_FILE_PATTERNS: set[str] = {"*report*.zip", "*report*.gz", "*dumpstate*.zip"}


CLI_HEADER = """
            ██████╗  ██████╗  ██████╗ ██╗     ██╗
            ██╔════╝ ██╔═══██╗██╔════╝██║     ██║
            ██║  ███╗██║   ██║██║     ██║     ██║
            ██║   ██║██║   ██║██║     ██║     ██║
            ╚██████╔╝╚██████╔╝╚██████╗███████╗██║
            ╚═════╝  ╚═════╝  ╚═════╝╚══════╝╚═╝
            - Developed by Govardhan Ummadisetty
            """

CLI_HEADER_1 = """
.----------------------------------------------------------------------------.
|██████╗ ██╗   ██╗ ██████╗ ██╗  ██╗████████╗██████╗  █████╗  ██████╗████████╗|
|██╔══██╗██║   ██║██╔════╝ ╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝|
|██████╔╝██║   ██║██║  ███╗ ╚███╔╝    ██║   ██████╔╝███████║██║        ██║   |
|██╔══██╗██║   ██║██║   ██║ ██╔██╗    ██║   ██╔══██╗██╔══██║██║        ██║   |
|██████╔╝╚██████╔╝╚██████╔╝██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗   ██║   |
|╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   |
'----------------------------------------------------------------------------'
                                          - Developed by Govardhan Ummadisetty    
"""

PACKAGE_PATTERN = r"Package \[(.*?)\]"
VERSION_NAME_PATTERN = r"versionName=(\S+)"
VERSION_CODE_PATTERN = r"versionCode=(\d+)"
LAST_UPDATE_TIME_PATTERN = r"lastUpdateTime=([\d\- :]+)"
TIME_ZONE_PATTERN = r"mEnvironment\.getDeviceTimeZone\(\)=([\w/]+)"

device_info_patterns: dict[str, Pattern[str]] = {
    "Serial": compile(pattern=r"\[ro\.serialno\]: \[([^\]]+)\]"),
    "Manufacturer": compile(pattern=r"\[ro\.product\.manufacturer\]: \[([^\]]+)\]"),
    "Model": compile(pattern=r"\[ro\.product\.model\]: \[([^\]]+)\]"),
    "Name": compile(pattern=r"\[ro\.product\.name\]: \[([^\]]+)\]"),
    "Build": compile(pattern=r"\[ro\.build\.description\]: \[([^\]]+)\]"),
    "Fingerprint": compile(pattern=r"\[ro\.(product|system)\.build\.fingerprint\]: \[([^\]]+)\]"),
    "Build date": compile(pattern=r"\[ro\.(product|system)\.build\.date\]: \[([^\]]+)\]"),
    "SDK Version": compile(pattern=r"\[ro\.build\.version\.sdk\]: \[([^\]]+)\]"),
    "Locale": compile(pattern=r"\[ro\.product\.locale\]: \[([^\]]+)\]"),
    "Device Timezone": compile(pattern=r"mEnvironment\.getDeviceTimeZone\(\)=([\w/]+)"),
    "WIFI Country Code": compile(pattern=r"\[ro\.boot\.wificountrycode\]: \[([^\]]+)\]"),
    "CPU Architecture": compile(pattern=r"\[ro\.product\.cpu\.abi\]: \[([^\]]+)\]"),
    "SOC Manufacturer": compile(pattern=r"\[ro\.soc\.manufacturer\]: \[([^\]]+)\]"),
    "SOC Model": compile(pattern=r"\[ro\.soc\.model\]: \[([^\]]+)\]"),
    # TODO: add last used application
}

other_info_patterns: dict[str, Pattern[str]] = {
    "Android ID": compile(pattern=r"AndroidId:\s([a-zA-Z0-9]+)"),
    "Onboarded Accounts": compile(pattern=r"Account\s\{name=(.+)@gmail\.com, type=com\.google\}"),
    "Device Uptime": compile(pattern=r"Uptime:\s(.+)"),
    "Boot Reason": compile(pattern=r"\[ro\.boot\.bootreason\]: \[([^\]]+)\]"),
    "Display Device": compile(pattern=r"deviceProductInfo=\{(.+)\}"),
}

bugreports: list[str] = []


def pattern_builder(dir_name: str, patterns: set[str]) -> set[str]:
    """Generates the file patterns

    Args:
        dir_path (str): Directory Name
        patterns (set[str]) file patterns for matching

    Returns:
        set[str]: set of path with file patterns

    """
    dir_path: str = os.path.join(os.path.expanduser(path="~"), dir_name)
    return {os.path.join(dir_path, pattern) for pattern in patterns if pattern}


def get_bugreports(dir_name: str) -> list[str]:
    """Fetches the list of bugreports

    Args:
        dir_name (str): Name of directory for lookup.

    Returns:
        list[str]: List of the bugreports sorted in recent order.
    """
    file_patterns: set[str] = pattern_builder(dir_name=dir_name, patterns=BUGREPORT_FILE_PATTERNS)
    time_stamp = lambda file: os.stat(path=file).st_mtime
    for file_format in file_patterns:
        bugreports.extend(glob.glob(pathname=file_format))
    return sorted(bugreports, key=time_stamp, reverse=True)


def select_bugreport(dir_name: str) -> Union[List[str], str]:
    """Prompt the user for selection.

    Args:
        dir_name (str): Directory name for file lookup.

    Returns:
        Union[List[str], str]: List of selected bugreports.
    """
    key_bindings: dict[str, list[dict[str, str]]] = {
        "toggle": [{"key": "right"}, {"key": "left"}],  # toggle choice and move down (tab)
        "answer": [{"key": "enter"}],  # answer the prompt
        "interrupt": [{"key": "c-c"}],  # raise KeyboardInterrupt
        "skip": [{"key": "c-z"}],  # skip the prompt
        "toggle-all": [{"key": "space"}],  # to select all the files
    }

    try:
        root_dir: str = os.path.join(os.path.expanduser("~"), dir_name)
        raw_files: List[str] = get_bugreports(dir_name=dir_name)
        bugreport_files: List[str] = [file.split(root_dir)[1] for file in raw_files if file]

        if len(bugreport_files) == 0:
            raise FileNotFoundError(f"No Bugreports in the {root_dir} directory")

        if len(bugreport_files) == 1:
            return raw_files

        selected_files = inquirer.fuzzy(  # type: ignore
            message="Select the Bugreports to proceed:",
            choices=bugreport_files,
            multiselect=True,
            keybindings=key_bindings,  # type: ignore
            mandatory=False,
            border=True,
            raise_keyboard_interrupt=True,
            transformer=lambda result: (
                f"selected {f"{count} bugreports" \
                if (count := len(result))> 1 else f"{count} bugreport"}."
            ),
        ).execute()

        if not selected_files:
            raise TypeError("Interrupted Selection")

        return [f"{root_dir}{file}" for file in selected_files if file]

    except (FileNotFoundError, TypeError) as e:
        print(e)
        return ""
    except KeyboardInterrupt as e:
        print("Interrupted selection", e)
        return ""


def _parse_file(file_path: str) -> tuple[str, str]:
    """parses the zip/gz files

    Args:
        file_path (str): zip/gz file path.
    """
    _file_path: str = ""
    if file_path.endswith(".gz"):
        tmp_file_path: str = f"{HOME}/.tmp.zip"
        with (
            open(file=tmp_file_path, mode="wb") as tmp_file,
            gzip.open(
                filename=file_path,
            ) as tmp_zip,
        ):
            tmp_file.write(tmp_zip.read())

        _file_path = tmp_file_path
    else:
        _file_path = file_path

    with ZipFile(file=_file_path) as bugreport_file:
        raw_bugreport_txt: str = [
            _ for _ in bugreport_file.namelist() if _.startswith("bugreport")
        ][0]

        with bugreport_file.open(name=raw_bugreport_txt) as dumpstate:
            dumpstate_txt: str = dumpstate.read().decode(encoding="utf-8", errors="replace")

    return (dumpstate_txt, raw_bugreport_txt)


def _handle_device_info(info_txt: str) -> dict:
    """Fetches device info from the dumpstate text.

    Args:
        info_txt (str): dumpstate text.

    Returns:
        dict: device info.
    """
    device_info: dict[Any, Any] = {}

    for info, pattern in device_info_patterns.items():
        match: Match[str] | None = search(pattern=pattern, string=info_txt)
        if match:
            if info in ("Fingerprint", "Build date"):
                device_info[info] = match.group(2)
            else:
                device_info[info] = match.group(1)

    return device_info


def _handle_other_info(info_txt: str) -> dict:
    """Fetches other info from the dumpstate text.

    Args:
        info_txt (str): dumpstate text.

    Returns:
        dict: other info.
    """
    other_info: dict[Any, Any] = {}

    for info, pattern in other_info_patterns.items():
        match: Match[str] | None = search(pattern=pattern, string=info_txt)
        if match:
            if info in ("Onboarded Accounts"):
                other_info[info] = match.group(1)
            else:
                other_info[info] = match.group(1)

    return other_info


def _handle_packages(info_txt: str) -> list[dict[str, Union[str, Any]]]:
    """Fetches the package name, version name, version code and last updatetime.

    Args:
        info_txt (str): dumpstate text

    Returns:
        list[dict[str, Union[str, Any]]]: package list.
    """
    package_info_list: list[Any] = []

    blocks: list[str] = info_txt.split(sep="Package [")

    for block in blocks[1:]:  # Skip the first split part as it does not contain a package
        block: str = (  # type: ignore
            "Package [" + block
        )  # Adding back the "Package [" for consistency

        package: Match[str] | None = search(pattern=PACKAGE_PATTERN, string=block)
        version_name: Match[str] | None = search(pattern=VERSION_NAME_PATTERN, string=block)
        version_code: Match[str] | None = search(pattern=VERSION_CODE_PATTERN, string=block)
        last_update_time: Match[str] | None = search(pattern=LAST_UPDATE_TIME_PATTERN, string=block)

        if package and version_name and version_code and last_update_time:
            package_info_list.append(
                {
                    "package": package.group(1),
                    "versionName": version_name.group(1),
                    "versionCode": version_code.group(1),
                    "lastUpdateTime": last_update_time.group(1),
                }
            )
    return package_info_list


def _generate_files(dumpstate_text: str, parsed_output_text: str, file_name: str):
    """Generates the rawbugreport and packageversion text files.

    Args:
        dumpstate_text (str): dumpstate text.
        parsed_output_text (str): text after parsing the raw dumpstate text.
        file_name (str): file name to be stored.
    """
    destination_path = f"{HOME}/reports"
    raw_bugreport_file_path = os.path.join(destination_path, file_name)
    package_version_file_path = raw_bugreport_file_path.replace("bugreport", "package_versions")
    if not os.path.exists(destination_path):
        os.makedirs(name=destination_path)

    with open(file=raw_bugreport_file_path, mode="w", encoding="utf-8") as write_raw_bugreport:
        write_raw_bugreport.write(dumpstate_text)

    with open(file=package_version_file_path, mode="w", encoding="utf-8") as package_versions:
        package_versions.write(parsed_output_text)


def parse_bugreport(file_path: str) -> None:
    """Parses the bugreport file

    Args:
        file_path (str): file path.
    """

    dumpstate_text, file_name = _parse_file(file_path=file_path)

    device_info: dict[Any, Any] = _handle_device_info(info_txt=dumpstate_text)

    other_info: dict[Any, Any] = _handle_other_info(info_txt=dumpstate_text)

    package_info_list: List[dict[str, str | Any]] = _handle_packages(info_txt=dumpstate_text)

    table = PrettyTable()
    table.field_names = ["Package", "Version Name", "Version Code", "Last Updated time"]
    table.sortby = "Package"
    table.align = "l"
    table._max_width = {"Version Name": 60}  # pylint: disable=W0212

    table.add_rows(rows=[list(pkg.values()) for pkg in package_info_list if pkg])

    table.title = f"List of packages in the {str(object=device_info.get("Name")).title()} device"

    device_info_str = "------------- Device Info -------------\n"
    for k, v in device_info.items():
        device_info_str += f"{k}: {v}\n"

    device_info_str += "---------------------------------------\n"

    other_info_str = "------------- Other Info -------------\n"
    for k, v in other_info.items():
        if "relativeAddress=[]" in v:
            continue
        other_info_str += f"{k}: {v}\n"

    other_info_str += "---------------------------------------\n"

    console.print(CLI_HEADER_1, justify="right")
    console.print(device_info_str)
    console.print(other_info_str)
    console.print(table)

    with console.capture() as capture:
        console.print(CLI_HEADER, justify="right", highlight=False)
        console.print(device_info_str, highlight=False)
        console.print(other_info_str, highlight=False)
        console.print(table, highlight=False)

    parsed_output = capture.get()

    _generate_files(
        dumpstate_text=dumpstate_text, parsed_output_text=parsed_output, file_name=file_name
    )


if __name__ == "__main__":
    files: List[str] | str = select_bugreport(dir_name="")
    for file in files:
        parse_bugreport(file_path=file)
