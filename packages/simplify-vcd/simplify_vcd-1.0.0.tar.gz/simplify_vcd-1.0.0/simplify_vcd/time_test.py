"""
This module contains unit tests for functions and classes used to parse and manipulate
time-related data from VCD (or Value-Change Dump) files.
"""

import click
import pytest

from simplify_vcd.time import (
    TIME_PARAM,
    Time,
    is_valid_time,
    multiplier_to_get_ns,
    parse_resolution,
    parse_time,
    parse_timescale_line,
)


def test_is_valid_time():
    """
    Tests the is_valid_time function with various valid time strings to ensure
    it returns True for properly formatted and supported inputs.
    """
    one_s = "1s"
    five_s = "5 s"
    one_ms = "1ms"
    five_ms = "5 ms"
    one_us = "1us"
    five_us = "5 us"
    one_ns = "1ns"
    five_ns = "5 ns"

    assert is_valid_time(one_s)
    assert is_valid_time(five_s)
    assert is_valid_time(one_ms)
    assert is_valid_time(five_ms)
    assert is_valid_time(one_us)
    assert is_valid_time(five_us)
    assert is_valid_time(one_ns)
    assert is_valid_time(five_ns)


def test_invalid_time():
    """
    Tests the is_valid_time function with various invalid time strings to ensure
    it returns False for improperly formatted, unsupported, or non-time inputs.
    """
    empty = ""
    one_spaced_s = " 1s "
    five_spaced_s = " 5 s "
    one_ps = "1ps"
    point_ns = "1.5ns"
    just_text = "hello, world"

    assert not is_valid_time(empty)
    assert not is_valid_time(one_spaced_s)
    assert not is_valid_time(five_spaced_s)
    assert not is_valid_time(one_ps)
    assert not is_valid_time(point_ns)
    assert not is_valid_time(just_text)


def test_valid_time_type():
    """
    Tests the TIME_PARAM function with various valid time strings to ensure they
    are correctly recognized and processed without errors.
    """
    one_s = TIME_PARAM("1s")
    five_s = TIME_PARAM("5 s")
    one_ms = TIME_PARAM("1ms")
    five_ms = TIME_PARAM("5 ms")
    one_us = TIME_PARAM("1us")
    five_us = TIME_PARAM("5 us")
    one_ns = TIME_PARAM("1ns")
    five_ns = TIME_PARAM("5 ns")

    assert one_s == "1s"
    assert five_s == "5 s"
    assert one_ms == "1ms"
    assert five_ms == "5 ms"
    assert one_us == "1us"
    assert five_us == "5 us"
    assert one_ns == "1ns"
    assert five_ns == "5 ns"


def test_invalid_time_type():
    """
    Tests the TIME_PARAM function with various invalid time strings to ensure it
    correctly raises exceptions with appropriate error messages.
    """
    with pytest.raises(click.BadParameter) as exception_info:
        TIME_PARAM("")
    assert "not a valid time" in str(exception_info.value)

    with pytest.raises(click.BadParameter) as exception_info:
        TIME_PARAM(" 1s ")
    assert "not a valid time" in str(exception_info.value)

    with pytest.raises(click.BadParameter) as exception_info:
        TIME_PARAM(" 5 s ")
    assert "not a valid time" in str(exception_info.value)

    with pytest.raises(click.BadParameter) as exception_info:
        TIME_PARAM("1ps")
    assert "not a valid time" in str(exception_info.value)

    with pytest.raises(click.BadParameter) as exception_info:
        TIME_PARAM("1.5ns")
    assert "not a valid time" in str(exception_info.value)

    with pytest.raises(click.BadParameter) as exception_info:
        TIME_PARAM("hello, world")
    assert "not a valid time" in str(exception_info.value)


def test_valid_parse_timescale_line():
    """
    Tests the parse_timescale_line function with valid inputs to ensure it correctly
    parses various timescale formats.

    The function checks cases with:
    - Standard formatting.
    - Extra spaces between values.
    - Tabs used as separators.
    """
    normal_timescale = "$timescale 1ns $end"
    spaced_timescale = " $timescale  10 us  $end "
    tabbed_timescale = "\t$timescale\t100\ts\t$end\t"

    parsed_normal = parse_timescale_line(normal_timescale)
    parsed_spaced = parse_timescale_line(spaced_timescale)
    parsed_tabbed = parse_timescale_line(tabbed_timescale)

    assert parsed_normal is not None
    assert parsed_normal.value == 1
    assert parsed_normal.unit == "ns"

    assert parsed_spaced is not None
    assert parsed_spaced.value == 10
    assert parsed_spaced.unit == "us"

    assert parsed_tabbed is not None
    assert parsed_tabbed.value == 100
    assert parsed_tabbed.unit == "s"


def test_invalid_parse_timescale_line():
    """
    Tests the parse_timescale_line function with invalid input cases to ensure it
    correctly returns None when the format is incorrect or unsupported.

    Invalid cases include:
    - Incorrect keyword in the line, instead of "$timescale".
    - Unsupported units like picoseconds.
    - Incorrect value; must only be 1, 10, or 100.
    """
    invalid_line = "$time 1ns $end"
    invalid_unit = "$timescale 10 ps $end"
    invalid_value = "$timescale 5ns $end"

    parsed_line = parse_timescale_line(invalid_line)
    parsed_unit = parse_timescale_line(invalid_unit)
    parsed_value = parse_timescale_line(invalid_value)

    assert parsed_line is None
    assert parsed_unit is None
    assert parsed_value is None


def test_valid_multiplier_to_get_ns():
    """
    Tests the multiplier_to_get_ns function with valid Time inputs to ensure
    the correct multiplier is returned for conversion to nanoseconds.

    The function verifies:
    - Conversion for seconds ('s').
    - Conversion for milliseconds ('ms').
    - Conversion for microseconds ('us').
    - Conversion for nanoseconds ('ns').
    """
    one_ns = Time(1, "ns")
    mult_one_ns = multiplier_to_get_ns(one_ns)
    assert mult_one_ns == 1.0

    two_us = Time(2, "us")
    mult_two_us = multiplier_to_get_ns(two_us)
    assert mult_two_us == 2_000.0

    five_ms = Time(5, "ms")
    mult_five_ms = multiplier_to_get_ns(five_ms)
    assert mult_five_ms == 5_000_000.0

    ten_s = Time(10, "s")
    mult_ten_s = multiplier_to_get_ns(ten_s)
    assert mult_ten_s == 10_000_000_000.0


def test_invalid_multiplier_to_get_ns():
    """
    Tests the multiplier_to_get_ns function with invalid Time inputs to ensure
    it correctly returns None for unsupported units.

    The function verifies:
    - Unsupported time unit like 'ps' (picoseconds).
    """
    invalid_unit = Time(1, "ps")
    invalid_unit_mult = multiplier_to_get_ns(invalid_unit)
    assert invalid_unit_mult is None


def test_parse_resolution():
    """
    Tests the parse_resolution function with various valid time resolution strings
    to ensure it correctly parses the numerical value and unit.
    """
    one_ms = "1ms"
    ten_us = "10us"
    hundred_s = "100s"

    parsed_one_ms = parse_resolution(one_ms)
    parsed_ten_us = parse_resolution(ten_us)
    parsed_hundred_s = parse_resolution(hundred_s)

    assert parsed_one_ms.value == 1
    assert parsed_one_ms.unit == "ms"
    assert parsed_ten_us.value == 10
    assert parsed_ten_us.unit == "us"
    assert parsed_hundred_s.value == 100
    assert parsed_hundred_s.unit == "s"


def test_invalid_parse_resolution():
    """
    Tests the parse_resolution function with invalid input cases to ensure it
    correctly returns None for improper formatting, unsupported units, or
    invalid time strings.
    """
    empty = ""
    one_spaced_s = " 1s "
    five_spaced_s = " 5 s "
    one_ps = "1ps"
    point_ns = "1.5ns"
    just_text = "hello, world"

    assert parse_resolution(empty) is None
    assert parse_resolution(one_spaced_s) is None
    assert parse_resolution(five_spaced_s) is None
    assert parse_resolution(one_ps) is None
    assert parse_resolution(point_ns) is None
    assert parse_resolution(just_text) is None


def test_parse_time():
    """
    Tests the parse_time function with valid time strings to ensure it correctly
    parses various formats of time values and their units.
    """
    one_ms = "1ms"
    five_ms = "5 ms"
    one_ns = "1ns"
    five_ns = "5 ns"

    parsed_one_ms = parse_time(one_ms)
    parsed_five_ms = parse_time(five_ms)
    parsed_one_ns = parse_time(one_ns)
    parsed_five_ns = parse_time(five_ns)

    assert parsed_one_ms.value == 1
    assert parsed_one_ms.unit == "ms"
    assert parsed_five_ms.value == 5
    assert parsed_five_ms.unit == "ms"
    assert parsed_one_ns.value == 1
    assert parsed_one_ns.unit == "ns"
    assert parsed_five_ns.value == 5
    assert parsed_five_ns.unit == "ns"


def test_invalid_parse_time():
    """
    Tests the parse_time function with invalid time strings to ensure that
    it correctly returns None for invalid formatting, unsupported units, or
    non-numerical input.
    """
    empty = ""
    one_spaced_s = " 1s "
    five_spaced_s = " 5 s "
    one_ps = "1ps"
    point_ns = "1.5ns"
    just_text = "hello, world"

    assert parse_time(empty) is None
    assert parse_time(one_spaced_s) is None
    assert parse_time(five_spaced_s) is None
    assert parse_time(one_ps) is None
    assert parse_time(point_ns) is None
    assert parse_time(just_text) is None
