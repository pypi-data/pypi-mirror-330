"""
This module contains unit tests for functions used to parse and print vcd files.
"""

import datetime

from simplify_vcd.time import Time
from simplify_vcd.vcd_file import build_header, get_timescale, strip_headers


def test_valid_get_timescale():
    """
    Test the get_timescale function to verify it correctly extracts a valid timescale
    from the given VCD data.
    """
    one_ns = ["$timescale 1 ns $end", "$enddefinitions $end"]
    assert get_timescale(one_ns) == Time(1, "ns")


def test_invalid_get_timescale():
    """
    Test the get_timescale function to verify behavior for invalid cases.
    """
    lines_without = [
        "$scope module vars $end",
        "$var wire 1 ! pin[0] $end",
        "$upscope $end",
        "$enddefinitions $end",
        "# 20",
        "1!",
    ]
    assert get_timescale(lines_without) is None

    lines_with_bad_spacing = [
        "  $timescale 1 ns $end",
        "$enddefinitions $end",
    ]
    assert get_timescale(lines_with_bad_spacing) is None


def test_strip_headers():
    """
    Test the strip_headers function to ensure it removes VCD headers correctly.
    """
    only_headers = [
        "$timescale 1 ns $end",
        "$scope module vars $end",
        "$var wire 1 ! pin[0] $end",
        "$upscope $end",
    ]
    assert not strip_headers(only_headers)

    only_data = ["#0", "0!", "#10", "1!"]
    assert strip_headers(only_data) == only_data

    headers_and_data = only_headers + only_data
    assert strip_headers(headers_and_data) == only_data


def test_build_header():
    """
    Test the build_header function with different inputs.
    """
    assert build_header(
        now=datetime.datetime(2000, 1, 1, 0, 0, 0),
        resolution=Time(1, "ns"),
        variables=["X", "Y", "Z"],
    ) == (
        "$date 2000-01-01 00:00:00 $end\n"
        "$timescale 1 ns $end\n"
        "$scope module values $end\n"
        "$var wire 1 X a $end\n"
        "$var wire 1 Y b $end\n"
        "$var wire 1 Z c $end\n"
        "$upscope $end\n"
        "$enddefinitions $end\n"
    )

    assert build_header(
        now=datetime.datetime(2000, 1, 1, 0, 0, 0),
        resolution=Time(1, "s"),
        variables=[],
    ) == (
        "$date 2000-01-01 00:00:00 $end\n"
        "$timescale 1 s $end\n"
        "$scope module values $end\n"
        "$upscope $end\n"
        "$enddefinitions $end\n"
    )
