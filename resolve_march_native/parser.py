# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

import re


_param_pattern = '--param [^ \\n]+'
_simple_pattern = '-[^ \\n]+'

_flag_matcher = re.compile('(?:%s|%s)' % (_param_pattern, _simple_pattern))


def extract_flags(text):
    start_marker_seen = False

    for line in text.split('\n'):
        if not (line.startswith('#') or line.startswith('@')):
            continue

        if not start_marker_seen:
            if 'options passed' in line:
                start_marker_seen = True
            else:
                continue

        for m in re.finditer(_flag_matcher, line):
            flag = m.group(0)
            if flag.startswith('-D'):
                continue

            yield flag
