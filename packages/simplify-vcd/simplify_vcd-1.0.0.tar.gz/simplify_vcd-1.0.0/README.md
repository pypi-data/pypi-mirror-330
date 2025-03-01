# Simplify VCD

> Clip, trim and reduce VCD files

Simplify VCD is a command-line tool designed to make working with Value
Change Dump (VCD) files more efficient and faster. VCD files can
quickly become large and unwieldy, making analysis and processing slow
and cumbersome. This tool enables users to clip sections of VCD files,
trim irrelevant data, and reduce the resolution to a more manageable
timescale, significantly improving processing speed and usability.

It started life as a simple script to convert the `analyzer` captures
from my Glasgow Digital Interface Explorer down to the micro-second
scale to speed up analysing them with Sigrok & Pulseview, but it grew
arms and legs until it became what you see in this repo.

I can't vouch it will play nicely with the VCDs produced by your
favorite tool, but it's managed fine with the captures I've made with
my Glasgow. Pull Requests to support other, more complicated, VCD files
are welcome!

## Install

```shell
$ pip install simplify-vcd
```

## Usage

### Snip a single frame from the stream and reduce the resolution

```shell
$ simplify-vcd \
    --truncate-before=124687us \
    --truncate-after=132000000ns \
    --output-timescale=1us \
    examples/input-1.vcd \
    examples/output-1.vcd

$ sigrok-cli -i examples/output-1.vcd -P uart:baudrate=9600,modbus | \
  grep modbus
modbus-1: Slave ID: 32
modbus-1: Function 3: Read Holding Registers
modbus-1: Byte count: 2
modbus-1: 0x0001 / 1
modbus-1: CRC correct
```

### Reduce the resolution to increase processing speed

```shell
$ time sigrok-cli -i examples/input-1.vcd -P uart:baudrate=9600,modbus
# ...
real    8m50.080s
user    8m49.770s
sys     0m0.129s

$ simplify-vcd \
    --output-timescale=1us \
    examples/input-1.vcd \
    examples/output-1.vcd

$ time sigrok-cli -i examples/output-1.vcd -P uart:baudrate=9600,modbus
# ...
real    0m0.663s
user    0m0.642s
sys     0m0.021s
```

## Development

```shell
# Create your virtual environment
$ python3 -m venv .venv --prompt=vcd

# Activate your virtual environment
$. .venv/bin/activate

# Install this code into your virtual environment as an editable
# package, with all our dev dependencies too
$ pip install -e .[dev]

#
# Do some coding...
#

# Lint and test
$ ./lint-and-test
```

## License

Simplify VCD - Clip, trim and reduce VCD files

Copyright (C) 2025 Mike Coats

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.
