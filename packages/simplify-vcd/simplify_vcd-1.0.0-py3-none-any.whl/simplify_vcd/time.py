"""
This module provides utility functions and classes for parsing, validating, and handling
time-related data from VCD (or Value-Change Dump) files.
"""

import re
from dataclasses import dataclass

import click
from click import Context, Parameter

TIME_PATTERN = r"^(\d+)\s*(s|ms|us|ns)$"


def is_valid_time(time: str) -> bool:
    """
    Is the string a valid time?

    The time string should follow the format: <integer><optional whitespace><unit>,
    where the unit is one of 's', 'ms', 'us', or 'ns'.

    Args:
        time (str): The time string to validate.

    Returns:
        bool: True if the time string is valid, False otherwise.
    """
    return bool(re.match(TIME_PATTERN, time))


class TimeParamType(click.ParamType):
    """
    A custom Click parameter type for validating and converting time strings.

    The time string should follow the format: <integer><optional whitespace><unit>,
    where the unit is one of 's', 'ms', 'us', or 'ns'.

    Attributes:
        name (str): The name of the parameter type, "time".

    Methods:
        convert(value, param, ctx):
            Validates the input value as a time string and returns it if valid.
            Fails with an error message if the value is invalid.
    """

    name = "time"

    def convert(
        self, value: str, param: Parameter | None, ctx: Context | None
    ) -> str | None:
        """
        Validates and converts the input time string.

        Args:
            value (str): The input time string to validate.
            param: The Click parameter object (not used here).
            ctx: The Click context object (not used here).

        Returns:
            str: The validated time string.

        Raises:
            click.BadParameter: If the input value is not a valid time string.
        """
        if is_valid_time(value):
            return value

        return self.fail(f"{value!r} is not a valid time", param, ctx)


TIME_PARAM = TimeParamType()


@dataclass
class Time:
    """
    Represents a time value with a specific unit.

    Attributes:
        value (int): The numerical value of the time.
        unit (str): The unit of the time, which can be one of 's' (seconds), 'ms'
                    (milliseconds), 'us' (microseconds), or 'ns' (nanoseconds).
    """

    value: int
    unit: str


def parse_time(time: str) -> Time | None:
    """
    Parses a time string and converts it into a Time object.

    The input string should follow the format: <integer><optional whitespace><unit>,
    where the unit is one of 's' (seconds), 'ms' (milliseconds), 'us' (microseconds),
    or 'ns' (nanoseconds).

    Args:
        time (str): The time string to parse.

    Returns:
        Time | None: A Time object with the parsed value and unit if valid; otherwise,
                     None.
    """
    match = re.fullmatch(TIME_PATTERN, time)
    if match:
        value, unit = match.groups()
        value = int(value)
        unit = unit.strip().lower()
        return Time(value, unit)
    return None


def parse_resolution(resolution: str) -> Time | None:
    """
    Parses and validates a resolution string to ensure it represents a valid time
    resolution.

    The resolution string should follow the format: <integer><optional whitespace>
    <unit>, where the integer value must be one of 1, 10, or 100, and the unit must be
    one of 's', 'ms', 'us', or 'ns'.

    Args:
        resolution (str): The resolution string to parse and validate.

    Returns:
        Time | None: A Time object with the parsed value and unit if valid; otherwise,
                     None.
    """
    time = parse_time(resolution)
    if time is not None and time.value in [1, 10, 100]:
        return time
    return None


def parse_timescale_line(timescale_line: str) -> Time | None:
    """
    Parses a VCD file timescale line and extracts the time resolution as a Time object.

    The timescale line should follow the format: $timescale <resolution> $end,
    where <resolution> is a valid time string, e.g., "1ns", "10us", etc.

    Args:
        timescale_line (str): The VCD file timescale line to parse.

    Returns:
        Time | None: A Time object representing the parsed time resolution if the line
                     is valid; otherwise, None.
    """
    timescale_pattern = r"^\s*\$timescale\s+(.*)\s+\$end\s*$"
    match = re.fullmatch(timescale_pattern, timescale_line)
    if match:
        time_string = match.group(1).strip()
        return parse_resolution(time_string)

    return None


def multiplier_to_get_ns(time: Time) -> float | None:
    """
    Computes a multiplier to convert a given time to nanoseconds.

    This function takes a Time object and returns a floating-point value
    that can be used to convert a timestamp expressed in the given time's
    unit to nanoseconds. If the unit is invalid, it returns None.

    Args:
        time (Time): A Time object containing a numerical value and a unit.
                     The unit must be one of 's' (seconds), 'ms' (milliseconds),
                     'us' (microseconds), or 'ns' (nanoseconds).

    Returns:
        float | None: The multiplier to convert the time to nanoseconds,
                      or None if the unit is invalid.
    """
    if time.unit == "ns":
        return time.value * 1.0
    if time.unit == "us":
        return time.value * 1.0e3
    if time.unit == "ms":
        return time.value * 1.0e6
    if time.unit == "s":
        return time.value * 1.0e9

    return None
