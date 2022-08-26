# Copyright (C) 2022 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

import re
import subprocess
from typing import List

# Example lines:
# "  -m128bit-long-double                  [enabled]"
# "  -m64                                  [enabled]"
_enabled_line_pattern = re.compile(r'^\s+(?P<flag>-[^ ]+)\s+\[enabled\]$')

# Example lines:
# "  -mincoming-stack-boundary=            0"
# "  -mindirect-branch=                    keep"
_value_line_pattern = re.compile(r'^\s+(?P<flag>-[^ =]+)=(?:<.+>)?\s+(?P<value>.*)$')

# Example lines:
# "  -mfused-madd                          -ffp-contract=fast"
# "  -mintel-syntax                        -masm=intel"
# "  -mprefer-avx128                       -mprefer-vector-width=128"
# "  -msse5                                -mavx"
_alias_line_pattern = re.compile(r'^\s+-\S+\s+(?P<flag>-[^ ]+)$')


def get_flags_implied_by_march(arch: str, gcc=None) -> List[str]:
    if gcc is None:
        gcc = 'gcc'
    argv = [gcc, '-Q', f'-march={arch}', '--help=target']
    gcc_output = subprocess.check_output(argv).decode('UTF-8')

    flags: List[str] = []

    for line in gcc_output.split('\n'):
        if not line.startswith('  -'):
            continue

        if line.endswith('[disabled]'):
            continue

        if line.endswith('[default]'):
            continue

        if line.endswith('[enabled]'):
            flag = _enabled_line_pattern.match(line).group('flag')
            flags.append(flag)
            continue

        alias_line_match = _alias_line_pattern.match(line)
        if alias_line_match is not None:
            flags.append(alias_line_match.group('flag'))
            continue

        value_line_match = _value_line_pattern.match(line)
        if value_line_match is not None:
            flag = value_line_match.group("flag") + '=' + value_line_match.group("value")
            flags.append(flag)
            continue

        raise ValueError(f'Line {line!r} not understood')

    return flags
