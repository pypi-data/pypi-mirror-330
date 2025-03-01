"""
This module provides utility functions for reading, processing, and generating VCD
(Value Change Dump) files.
"""

from datetime import datetime

from simplify_vcd.time import Time, parse_timescale_line


def get_timescale(vcd_data: list[str]) -> Time | None:
    """
    Extracts the timescale from a given VCD file.

    Args:
        vcd_data (list[str]): The lines of a VCD file as a list of strings.

    Returns:
        Time | None: A Time object representing the timescale if found, otherwise None.
    """
    timescale_line = next(
        (line for line in vcd_data if line.startswith("$timescale")), None
    )

    if timescale_line:
        return parse_timescale_line(timescale_line)

    return None


def strip_headers(vcd_data: list[str]) -> list[str]:
    """
    Removes the header lines from a VCD file's data.

    Args:
        vcd_data (list[str]): The lines of a VCD file as a list of strings.

    Returns:
        list[str]: The VCD data with headers removed. If only headers are present, an
                   empty list is returned.
    """
    last_header_line = -1
    for i, line in enumerate(vcd_data):
        if line.strip().startswith("$"):
            last_header_line = i

    if last_header_line == len(vcd_data) - 1:
        return []

    if last_header_line != -1:
        return vcd_data[last_header_line + 1 :]

    return vcd_data


def build_header(now: datetime, resolution: Time, variables: list[str]) -> str:
    """
    Builds the header section of a VCD file.

    Args:
        now (datetime): The current date and time to include in the header.
        resolution (Time): The time resolution to include in the header (value and
                           unit).
        variables (list[str]): A list of variable names to define in the header.

    Returns:
        str: The formatted VCD file header as a multi-line string.
    """
    date = f"$date {str(now)} $end"
    timescale = f"$timescale {resolution.value} {resolution.unit} $end"
    scope = "$scope module values $end"
    variables = [
        f"$var wire 1 {variable} {chr(97 + i)} $end"
        for i, variable in enumerate(variables)
    ]
    end_scope = "$upscope $end"
    end_header = "$enddefinitions $end"
    return "\n".join([date, timescale, scope] + variables + [end_scope, end_header, ""])
