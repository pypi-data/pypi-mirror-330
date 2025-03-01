"""
Simplifies a VCD (Value Change Dump) file by truncating data to a specified time
range, rescaling timestamps to a new timescale, and merging coincident changes.
"""

import sys
from datetime import datetime

import click

from simplify_vcd.changes import (
    get_variables,
    merge_changes,
    parse_changes,
    re_align_changes,
    scale_changes,
    trim_after_end,
    trim_before_start,
)
from simplify_vcd.time import (  # parse_time,
    TIME_PARAM,
    Time,
    multiplier_to_get_ns,
    parse_resolution,
    parse_time,
)
from simplify_vcd.vcd_file import build_header, get_timescale, strip_headers


@click.command()
@click.option("--output-timescale", type=TIME_PARAM, help="Timescale of output")
@click.option(
    "--truncate-before",
    type=TIME_PARAM,
    help="Truncate before this time",
)
@click.option(
    "--truncate-after",
    type=TIME_PARAM,
    help="Truncate after this time",
)
@click.argument("input_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
def simplify(
    output_timescale, truncate_before, truncate_after, input_file, output_file
):
    """
    Simplifies a VCD (Value Change Dump) file by truncating data to a specified time
    range, rescaling timestamps to a new timescale, and merging coincident changes.

    Args:
        output_timescale (str): The desired timescale for the output VCD file.
        truncate_before (str): The start time to truncate changes. Changes before this
                               time are removed.
        truncate_after (str): The end time to truncate changes. Changes after this time
                              are removed.
        input_file (file): The input VCD file containing the data to process.
        output_file (file): The processed VCD file to write the simplified data to.

    Returns:
        None
    """

    vcd_data = input_file.readlines()
    if len(vcd_data) == 0:
        print("Error: VCD file is empty.", file=sys.stderr)
        sys.exit(1)

    input_timescale = get_timescale(vcd_data)
    if input_timescale is None:
        print("Error: VCD file does not have a timescale.", file=sys.stderr)
        sys.exit(1)

    vcd_data = strip_headers(vcd_data)
    if len(vcd_data) == 0:
        print("Error: VCD file has no data.", file=sys.stderr)
        sys.exit(1)

    # Read in and re-scale the timestamps to nanoseconds.
    ns_changes = scale_changes(
        parse_changes(vcd_data),
        multiplier_to_get_ns(input_timescale),
    )

    # Remove the changes before the start time.
    if truncate_before:
        start = parse_time(truncate_before)
        ns_changes = trim_before_start(ns_changes, start)

    # Remove the changes after the end time.
    if truncate_after:
        end = parse_time(truncate_after)
        ns_changes = trim_after_end(ns_changes, end)

    # Re-scale our nanosecond timestamps to our output resolution.
    if output_timescale:
        ns_changes = scale_changes(
            ns_changes,
            1 / multiplier_to_get_ns(parse_resolution(output_timescale)),
        )

    # Shift changes to a new 0-point.
    if truncate_before:
        ns_changes = re_align_changes(ns_changes)

    # Merge any co-incident changes on our new resolution's timeline.
    ns_changes = merge_changes(ns_changes)

    # Find all the variables in our output changes.
    variables = get_variables(ns_changes)

    # Write out the file header.
    output_file.writelines(
        build_header(
            datetime.now(),
            parse_resolution(output_timescale) if output_timescale else Time(1, "ns"),
            variables,
        )
    )

    # Write out the file data.
    for change in ns_changes:
        output_file.writelines(str(change))


if __name__ == "__main__":
    # We pass our `argv` to `click` to sort out for us, so we don't expect to directly
    # set each parameter here.
    # pylint: disable=no-value-for-parameter
    simplify(sys.argv[1:])
    # pylint: enable=no-value-for-parameter
