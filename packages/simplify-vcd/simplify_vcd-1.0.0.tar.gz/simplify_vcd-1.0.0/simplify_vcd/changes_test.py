"""
This module contains unit tests for functions and classes used to parse and manipulate
changes in variables' values over time.
"""

from functools import reduce

import pytest

from simplify_vcd.changes import (
    Change,
    TimedChange,
    get_variables,
    merge_changes,
    merge_coincident_changes,
    parse_changes,
    re_align_changes,
    scale_changes,
    trim_after_end,
    trim_before_start,
)
from simplify_vcd.time import Time


def test_change_str():
    """
    Tests the string representation of the Change class.
    Ensures that the __str__ method correctly formats the variable and value.
    """
    c1 = Change("a", True)
    c2 = Change("b", False)

    assert str(c1) == "1a\n"
    assert str(c2) == "0b\n"


def test_timed_change_str():
    """
    Tests the string representation of the TimedChange class.
    Ensures that the __str__ method correctly formats the timestamp and changes.
    """
    tc1 = TimedChange(1000, [Change("a", True)])
    assert str(tc1) == "#1000\n1a\n"

    tc2 = TimedChange(1003, [Change("a", True), Change("b", False)])
    assert str(tc2) == "#1003\n1a\n0b\n"


def test_valid_coincident_changes():
    """
    Tests the merge_coincident_changes function for valid cases.
    Ensures that changes with the same timestamp are merged correctly,
    and updates to the same variable prioritize the second change provided.
    """
    a_1 = Change("a", False)
    b_1 = Change("b", False)
    a_2 = Change("a", True)

    c_a_1 = TimedChange(0, [a_1])
    c_b_1 = TimedChange(0, [b_1])
    c_a_2 = TimedChange(0, [a_2])

    c_m_ab_1 = merge_coincident_changes(c_a_1, c_b_1)
    assert c_m_ab_1.timestamp == 0
    assert len(c_m_ab_1.values) == 2
    assert c_m_ab_1.values[0].variable == "a"
    assert c_m_ab_1.values[0].value is False
    assert c_m_ab_1.values[1].variable == "b"
    assert c_m_ab_1.values[1].value is False

    c_m_a_12 = merge_coincident_changes(c_a_1, c_a_2)
    assert c_m_a_12.timestamp == 0
    assert len(c_m_a_12.values) == 1
    assert c_m_a_12.values[0].variable == "a"
    assert c_m_a_12.values[0].value is True

    c_ab_11 = TimedChange(1234, [a_1, b_1])
    c_ba_12 = TimedChange(1234, [b_1, a_2])
    cm_aba_112 = merge_coincident_changes(c_ab_11, c_ba_12)
    assert cm_aba_112.timestamp == 1234
    assert len(cm_aba_112.values) == 2
    assert cm_aba_112.values[0].variable == "a"
    assert cm_aba_112.values[0].value is True
    assert cm_aba_112.values[1].variable == "b"
    assert cm_aba_112.values[1].value is False


def test_invalid_coincident_changes():
    """
    Tests the merge_coincident_changes function for invalid cases.
    Ensures that an error is raised when the timestamps do not match.
    """
    a_1 = Change("a", False)
    b_1 = Change("b", False)

    c_a_1 = TimedChange(0, [a_1])
    c_b_1 = TimedChange(1, [b_1])
    with pytest.raises(ValueError) as exception_info:
        merge_coincident_changes(c_a_1, c_b_1)
    assert "do not match" in str(exception_info.value)


def test_scale_changes():
    """
    Tests the scale_changes function to ensure timestamps are scaled correctly
    and associated changes are preserved.
    """
    tc_1 = TimedChange(1000, [Change("a", False), Change("b", False)])
    tc_2 = TimedChange(1003, [Change("a", True), Change("b", True)])
    scaled_changes = scale_changes([tc_1, tc_2], 0.001)

    assert len(scaled_changes) == 2

    assert scaled_changes[0].timestamp == 1
    assert len(scaled_changes[0].values) == 2
    assert scaled_changes[0].values[0].variable == "a"
    assert scaled_changes[0].values[0].value is False
    assert scaled_changes[0].values[1].variable == "b"
    assert scaled_changes[0].values[1].value is False

    assert scaled_changes[1].timestamp == 1
    assert len(scaled_changes[1].values) == 2
    assert scaled_changes[1].values[0].variable == "a"
    assert scaled_changes[1].values[0].value is True
    assert scaled_changes[1].values[1].variable == "b"
    assert scaled_changes[1].values[1].value is True


def test_scale_and_merge_changes():
    """
    Tests the combination of scaling and merging changes.
    Ensures that timestamps are scaled correctly and coincident changes are merged
    properly.
    """
    tc_1 = TimedChange(1000, [Change("a", False), Change("b", False)])
    tc_2 = TimedChange(1003, [Change("a", True), Change("b", True)])
    scaled_changes = scale_changes([tc_1, tc_2], 0.001)
    merged_changes = reduce(merge_coincident_changes, scaled_changes)

    assert merged_changes is not None

    assert merged_changes.timestamp == 1
    assert len(merged_changes.values) == 2
    assert merged_changes.values[0].variable == "a"
    assert merged_changes.values[0].value is True
    assert merged_changes.values[1].variable == "b"
    assert merged_changes.values[1].value is True


def test_re_align_changes():
    """
    Tests the re_align_changes function to ensure proper alignment of timestamps
    after scaling or adjustments in time intervals.
    """
    tc_1 = TimedChange(1000, [Change("a", False)])
    tc_2 = TimedChange(2000, [Change("a", True)])

    aligned_changes = re_align_changes([tc_1, tc_2])

    assert len(aligned_changes) == 2

    assert aligned_changes[0].timestamp == 0
    assert len(aligned_changes[0].values) == 1
    assert aligned_changes[0].values[0].variable == "a"
    assert aligned_changes[0].values[0].value is False

    assert aligned_changes[1].timestamp == 1000
    assert len(aligned_changes[1].values) == 1
    assert aligned_changes[1].values[0].variable == "a"
    assert aligned_changes[1].values[0].value is True


def test_trim_after_end():
    """
    Tests the trim_after_end function to ensure proper trimming of changes that
    occur on or after a specified end timestamp.
    """
    changes = [
        TimedChange(0, [Change("a", False)]),
        TimedChange(10, [Change("a", True)]),
        TimedChange(20, [Change("a", False)]),
    ]

    trimmed_on = trim_after_end(changes, Time(10, "ns"))
    assert trimmed_on == [
        TimedChange(0, [Change("a", False)]),
        TimedChange(10, [Change("a", True)]),
    ]

    trimmed_between = trim_after_end(changes, Time(15, "ns"))
    assert trimmed_between == [
        TimedChange(0, [Change("a", False)]),
        TimedChange(10, [Change("a", True)]),
        TimedChange(15, [Change("a", True)]),
    ]

    trimmed_at_first = trim_after_end(changes, Time(0, "ns"))
    assert trimmed_at_first == [TimedChange(0, [Change("a", False)])]


def test_trim_before_start():
    """
    Tests the trim_before_start function to ensure proper trimming of changes that
    occur beforeor on a specified start timestamp.
    """
    changes = [
        TimedChange(0, [Change("a", False)]),
        TimedChange(10, [Change("a", True)]),
        TimedChange(20, [Change("a", False)]),
    ]

    trimmed_on = trim_before_start(changes, Time(10, "ns"))
    assert trimmed_on == [
        TimedChange(10, [Change("a", True)]),
        TimedChange(20, [Change("a", False)]),
    ]

    trimmed_between = trim_before_start(changes, Time(5, "ns"))
    assert trimmed_between == [
        TimedChange(5, [Change("a", False)]),
        TimedChange(10, [Change("a", True)]),
        TimedChange(20, [Change("a", False)]),
    ]

    trimmed_at_last = trim_before_start(changes, Time(20, "ns"))
    assert trimmed_at_last == [TimedChange(20, [Change("a", False)])]


def test_get_variables():
    """
    Tests the get_variables function to ensure the correct extraction of unique
    variable names from a list of TimedChange objects.
    """
    changes = [
        TimedChange(0, [Change("a", False), Change("b", False)]),
        TimedChange(10, [Change("b", True), Change("c", False)]),
        TimedChange(15, [Change("b", False), Change("c", True)]),
    ]
    variables = get_variables(changes)
    assert len(variables) == 3
    assert "a" in variables
    assert "b" in variables
    assert "c" in variables

    empty = []
    variables = get_variables(empty)
    assert not variables


def test_merge_changes():
    """
    Tests the merge_changes function to ensure that TimedChange objects with
    the same timestamp are combined correctly, preserving all variable changes.
    """
    changes = [
        TimedChange(0, [Change("a", False)]),
        TimedChange(0, [Change("b", False)]),
        TimedChange(10, [Change("b", True)]),
        TimedChange(15, [Change("b", False)]),
        TimedChange(15, [Change("c", True)]),
    ]

    merged = merge_changes(changes)

    assert len(merged) == 3
    assert merged[0].timestamp == 0
    assert len(merged[0].values) == 2
    assert merged[1].timestamp == 10
    assert len(merged[1].values) == 1
    assert merged[2].timestamp == 15
    assert len(merged[2].values) == 2

    empty = merge_changes([])
    assert not empty


def test_parse_changes():
    """
    Tests the parse_changes function to ensure that it correctly parses input lines
    into TimedChange objects with appropriate timestamps and variable changes.
    """
    input_lines = ["#10", "1a", "0b", "#20", "1b"]

    changes = parse_changes(input_lines)

    assert len(changes) == 2

    assert changes[0].timestamp == 10
    assert len(changes[0].values) == 2
    assert changes[0].values[0].variable == "a"
    assert changes[0].values[0].value is True
    assert changes[0].values[1].variable == "b"
    assert changes[0].values[1].value is False

    assert changes[1].timestamp == 20
    assert len(changes[1].values) == 1
    assert changes[1].values[0].variable == "b"
    assert changes[1].values[0].value is True
