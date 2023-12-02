# Copyright (C) 2022 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

import os
import re
import subprocess
import sys
from typing import List

from .environment import enforce_c_locale

# Example lines:
# "  -m128bit-long-double                  [enabled]"
# "  -m64                                  [enabled]"
_enabled_line_pattern = re.compile(r'^\s+(?P<flag>-[^ ]+)\s+\[enabled\]$')

# Example lines:
# "  -mavx                                 [disabled]"
# "  -mno-align-stringops        \t\t[disabled]"
_disabled_m_line_pattern = re.compile(r'^\s+(?P<flag>-m[^ ]+)\s+\[disabled\]$')

# Example lines:
# "  -mgen-cell-microcode        \t\t[ignored]"
_ignore_marked_line_pattern = re.compile(r'^\s+(?P<flag>-[^ ]+)\s+\[ignored\]$')

# Example lines:
# "  -mincoming-stack-boundary=            0"
# "  -mindirect-branch=                    keep"
_assign_value_line_pattern = re.compile(r'^\s+(?P<flag>-[^ =]+)=(?:<.+>)?\s+(?P<value>.*)$')

# Example lines:
# "  -mabi=ABI                   \t\tlp64"
_assign_var_value_line_pattern = re.compile(r'^\s+(?P<flag>-[^ =]+)=[A-Z]+\s+(?P<value>.*)$')

# Example lines:
# "  -msdata=[none,data,sysv,eabi] \tnone"
_array_value_line_pattern = re.compile(r'^\s+(?P<flag>-[^ =]+)=\[.+\]\s+(?P<value>.*)$')

# Example lines:
# "  -mtarget-linker <version>   \t\t711"
_space_value_line_pattern = re.compile(r'^\s+(?P<flag>-[^ =]+) <[^>]+>\s+(?P<value>.*)$')

# Example lines:
# "  -G<number>                  \t\t8"
_value_line_pattern = re.compile(r'^\s+(?P<flag>-[^ =<]+)<[^>]+>\s+(?P<value>.*)$')

# Example lines:
# "  -malign-                    \t\tnatural"
_concat_arg_line_pattern = re.compile(r'^\s+(?P<flag>-[^ =]+-)\s+(?P<value>.+)$')

# Example lines:
# "  -mcall-ABI                  \t\tlinux"
_concat_var_line_pattern = re.compile(r'^\s+(?P<flag>-[^ =]+-)[A-Z]+\s+(?P<value>.+)$')

# Example lines:
# "  -mfused-madd                \t\t"
# "  -mintel-syntax              \t\t"
# "  -msse5                      \t\t"
_deprecated_or_removed_line_pattern = re.compile(r'^\s+(?P<flag>-[^ =]+)\s+$')

# Example lines:
# "  -mfused-madd                          -ffp-contract=fast"
# "  -mintel-syntax                        -masm=intel"
# "  -mprefer-avx128                       -mprefer-vector-width=128"
# "  -msse5                                -mavx"
_alias_line_pattern = re.compile(r'^\s+-\S+\s+(?P<flag>-[^ ]+)$')

# Example lines:
# "  -iframework <dir>           \t\t"
_ignore_line_pattern = re.compile(r'^\s+-iframework <dir>\s+$')


def get_flags_implied_by_march(arch: str, gcc=None, debug=True) -> List[str]:
    if gcc is None:
        gcc = 'gcc'
    base_argv = [gcc, '-Q', '--help=target']
    env = os.environ.copy()
    stderr = None if debug else subprocess.DEVNULL
    enforce_c_locale(env)
    try:
        cmd = base_argv + [f'-march={arch}']
        if debug:
            print('# %s' % ' '.join(cmd), file=sys.stderr)
        gcc_output = subprocess.check_output(cmd, env=env, stderr=stderr).decode('UTF-8')
    except subprocess.CalledProcessError:
        cmd = base_argv + [f'-mcpu={arch}']
        if debug:
            print('# %s' % ' '.join(cmd), file=sys.stderr)
        gcc_output = subprocess.check_output(cmd, env=env, stderr=stderr).decode('UTF-8')
    return _parse_gcc_output(gcc_output)


def _parse_gcc_output(gcc_output: str) -> List[str]:
    flags: List[str] = []

    for line in gcc_output.split('\n'):
        if not line.startswith('  -'):
            continue

        if line.endswith('[default]'):
            continue

        if line.endswith('[available in C++]'):  # on macOS
            continue

        if line.endswith('[enabled]'):
            flag = _enabled_line_pattern.match(line).group('flag')
            flags.append(flag)
            continue

        if line.endswith('[disabled]'):
            flag = _disabled_m_line_pattern.match(line).group('flag')
            if flag.startswith('-mno-'):
                # Drop the "no"
                flags.append('-m' + flag[len('-mno-'):])
            else:
                flags.append('-mno-' + flag[len('-m'):])
            continue

        if line.endswith('[ignored]'):
            flag = _ignore_marked_line_pattern.match(line).group('flag')
            flags.append(flag)
            continue

        ignore_line_match = _ignore_line_pattern.match(line)
        if ignore_line_match is not None:
            continue

        deprecated_line_match = _deprecated_or_removed_line_pattern.match(line)
        if deprecated_line_match is not None:
            continue

        alias_line_match = _alias_line_pattern.match(line)
        if alias_line_match is not None:
            continue

        value_line_match = _assign_value_line_pattern.match(line)
        if value_line_match is not None:
            flag = value_line_match.group("flag") + '=' + value_line_match.group("value")
            flags.append(flag)
            continue

        value_line_match = _assign_var_value_line_pattern.match(line)
        if value_line_match is not None:
            flag = value_line_match.group("flag") + '=' + value_line_match.group("value")
            flags.append(flag)
            continue

        value_line_match = _array_value_line_pattern.match(line)
        if value_line_match is not None:
            flag = value_line_match.group("flag") + '=' + value_line_match.group("value")
            flags.append(flag)
            continue

        value_line_match = _space_value_line_pattern.match(line)
        if value_line_match is not None:
            flag = value_line_match.group("flag") + ' ' + value_line_match.group("value")
            flags.append(flag)
            continue

        value_line_match = _value_line_pattern.match(line)
        if value_line_match is not None:
            flag = value_line_match.group("flag") + value_line_match.group("value")
            flags.append(flag)
            continue

        concat_arg_line_match = _concat_arg_line_pattern.match(line)
        if concat_arg_line_match is not None:
            flag = concat_arg_line_match.group("flag") + concat_arg_line_match.group("value")
            flags.append(flag)
            continue

        concat_var_line_match = _concat_var_line_pattern.match(line)
        if concat_var_line_match is not None:
            flag = concat_var_line_match.group("flag") + concat_var_line_match.group("value")
            flags.append(flag)
            continue

        raise ValueError(f'Line {line!r} not understood')

    return flags
