"""
This module provides utility functions and classes for parsing, validating, and handling
changes in variables' values over time.
"""

from dataclasses import dataclass

from simplify_vcd.time import Time, multiplier_to_get_ns


@dataclass
class Change:
    """
    Represents a change in the value of a variable in a VCD file.

    Attributes:
        variable (str): The name of the variable to which the change applies.
        value (bool): The new value of the variable (True for '1', False for '0').
    """

    variable: str
    value: bool

    def __str__(self):
        """
        Converts the Change object to a string representation for output.

        Returns:
            str: A string in the format '1<variable>' if value is True,
                 or '0<variable>' if value is False, followed by a newline.
        """
        return f"{1 if self.value else 0}{self.variable}\n"


@dataclass
class TimedChange:
    """
    Represents a timed change in a VCD file.

    Attributes:
        timestamp (int): The timestamp of the change.
        values (list[Change]): A list of Change objects representing the variable
                               changes at this timestamp.
    """

    timestamp: int
    values: list[Change]

    def __str__(self) -> str:
        """
        Converts the TimedChange object to a string representation.

        Returns:
            str: A string in the format '#<timestamp>' followed by the string
                 representations of each Change in the values list, each on a new line.
        """
        return f"#{self.timestamp}\n{''.join([str(val) for val in self.values])}"


def parse_changes(vcd_data: list[str]) -> list[TimedChange]:
    """
    Parses VCD (Value Change Dump) data and groups changes into timed blocks.

    This function iterates over lines of VCD data, extracting timestamps and
    associated changes in variable values. It groups these changes into
    TimedChange objects, which represent the changes occurring at each
    specific timestamp.

    Args:
        vcd_data (list[str]): A list of strings representing the lines of a VCD file.

    Returns:
        list[TimedChange]: A list of TimedChange objects, where each object
                           contains a timestamp and the respective changes
                           occurring at that timestamp.

    Example:
        Input VCD data:
            [
                '#10',
                '1a',
                '0b',
                '#20',
                '1b'
            ]

        Output:
            [
                TimedChange(timestamp=10, values=[
                    Change(variable='a', value=True),
                    Change(variable='b', value=False)
                ]),
                TimedChange(timestamp=20, values=[
                    Change(variable='b', value=True)
                ])
            ]
    """
    changes = []
    current_timestamp = None
    current_changes = []
    for line in vcd_data:
        if line.startswith("#"):
            if current_timestamp is not None:
                changes.append(TimedChange(int(current_timestamp), current_changes))
            current_timestamp = int(line[1:])
            current_changes = []

        elif current_timestamp:
            value = line[0] == "1"
            variable = line[1:].strip()
            current_changes.append(Change(variable, value))

    if current_changes:
        changes.append(TimedChange(int(current_timestamp), current_changes))

    return changes


def scale_changes(changes: list[TimedChange], scale: float) -> list[TimedChange]:
    """
    Scales the timestamps of a list of TimedChange objects by a given factor.

    This is used to adjust the resolution of timestamps in VCD files. For example,
    scaling with a factor of 0.001 can convert timestamps from nanoseconds (ns)
    to microseconds (us).

    Args:
        changes (list[TimedChange]): A list of TimedChange objects to be scaled.
        scale (float): The scaling factor for the timestamps.

    Returns:
        list[TimedChange]: A new list of TimedChange objects with scaled timestamps,
                           preserving the original order and values.
    """
    scaled_changes = [
        TimedChange(int(change.timestamp * scale), change.values) for change in changes
    ]
    return scaled_changes


def re_align_changes(changes: list[TimedChange]) -> list[TimedChange]:
    """
    Re-aligns the timestamps of a list of TimedChange objects to start from zero.

    This function adjusts the timestamps of all TimedChange objects so that the first
    change begins at timestamp zero. This is achieved by subtracting the timestamp of
    the first change from all timestamps.

    Args:
        changes (list[TimedChange]): A list of TimedChange objects to be re-aligned.

    Returns:
        list[TimedChange]: A new list of TimedChange objects with adjusted timestamps,
                           where the first change starts at timestamp zero.
    """
    start = changes[0].timestamp
    re_aligned_changes = [
        TimedChange(int(change.timestamp - start), change.values) for change in changes
    ]
    return re_aligned_changes


def merge_coincident_changes(change1: TimedChange, change2: TimedChange) -> TimedChange:
    """
    Merges two TimedChange objects with the same timestamp.

    This is useful for combining multiple changes at the same timestamp, which can
    happen after reducing the resolution of a VCD file from nanoseconds to microseconds
    for example.

    Args:
        change1 (TimedChange): The first timed change object.
        change2 (TimedChange): The second timed change object, must have the same
                               timestamp as change1.

    Returns:
        TimedChange: A new TimedChange object containing combined changes from both
                     inputs, with the second object's changes taking precedence in case
                     of conflicts.
    """
    if change1.timestamp != change2.timestamp:
        raise ValueError("Timestamps do not match for merging")

    value_map = {change.variable: change.value for change in change1.values}
    for change in change2.values:
        value_map[change.variable] = change.value

    merged_values = [Change(variable, value) for variable, value in value_map.items()]
    return TimedChange(change1.timestamp, merged_values)


def get_variables(ns_changes: list[TimedChange]) -> list[str]:
    """
    Extracts a list of unique variable names from a list of TimedChange objects.

    Args:
        ns_changes (list[TimedChange]): A list of TimedChange objects that contain
                                        variable changes.

    Returns:
        list[str]: A list of unique variable names extracted from the changes.
    """
    variables = set()
    for change in ns_changes:
        for var in change.values:
            variables.add(var.variable)
    return list(variables)


def merge_changes(changes: list[TimedChange]) -> list[TimedChange]:
    """
    Merges a list of TimedChange objects by combining changes that occur at the same
    timestamp into a single TimedChange.

    Args:
        changes (list[TimedChange]): The list of TimedChange objects to merge.

    Returns:
        list[TimedChange]: A list of TimedChange objects with no duplicate timestamps,
                           where coincident changes have been merged.
    """
    merged_changes: list[TimedChange] = []
    for i, _ in enumerate(changes):
        if i > 0 and changes[i].timestamp == merged_changes[-1].timestamp:
            merged_changes[-1] = merge_coincident_changes(
                merged_changes[-1], changes[i]
            )
        else:
            merged_changes.append(changes[i])
    return merged_changes


def trim_before_start(changes: list[TimedChange], start_ts: Time) -> list[TimedChange]:
    """
    Filters changes to keep only those occurring after the specified start time. If the
    start time is between changes, add a re-aligned copy of the prior change before
    cut-off.

    Args:
        changes (list[TimedChange]): The list of changes with their timestamps.
        start_ts (Time): The start time as a Time object.

    Returns:
        list[TimedChange]: A list of changes starting from the start time.
    """
    start = int(multiplier_to_get_ns(start_ts))

    kept = [change for change in changes if change.timestamp >= start]

    # If we start on a change, return from and including that change.
    if kept[0].timestamp == start:
        return kept

    # If we start between changes, create a duplicated value at the trim point
    previous_change_idx = changes.index(kept[0]) - 1
    state_before_truncate = TimedChange(start, changes[previous_change_idx].values)
    # Return the extra point and all the changes from and including the first change.
    return [state_before_truncate] + kept


def trim_after_end(changes: list[TimedChange], end_ts: Time) -> list[TimedChange]:
    """
    Filters changes to keep only those occurring before the specified end time. If the
    end time is between changes, duplicate the last change at the end time.

    Args:
        changes (list[TimedChange]): The list of changes with their timestamps.
        end_ts (Time): The end time as a Time object.

    Returns:
        list[TimedChange]: A list of changes up to the end time.
    """
    end = int(multiplier_to_get_ns(end_ts))

    kept = [change for change in changes if change.timestamp <= end]

    # If we stop on a change, return up to and including that change.
    if kept[-1].timestamp == end:
        return kept

    # If we stop between changes, create a duplicated value at the trim point
    state_after_truncate = TimedChange(end, kept[-1].values)
    # Return all the changes up to and including the last change plus the extra point.
    return kept + [state_after_truncate]
