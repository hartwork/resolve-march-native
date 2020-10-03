#! /usr/bin/env python
# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

import argparse
import signal
import sys
import traceback
from textwrap import dedent

from .engine import Engine
from .recommended import add_recommended_flags
from .sort import flags_sort_key
from .version import VERSION_STR

_HORIZONTAL, _VERTICAL = range(2)


def _inner_main():
    parser = argparse.ArgumentParser(
        prog='resolve-march-native',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent("""\
                %(prog)s is software libre licensed under GPL v2 or later,
                written by Sebastian Pipping.  Please report bugs to
                https://github.com/hartwork/resolve-march-native/issues.  Thanks!
                """),
    )
    parser.add_argument('--debug', action='store_true',
                        help='enable debugging (default: disabled)')
    parser.add_argument('--gcc', default='gcc', metavar='COMMAND',
                        help='gcc command (default: %(default)s)')
    parser.add_argument('--vertical', dest='formatting',
                        default=_HORIZONTAL, action='store_const', const=_VERTICAL,
                        help='produce vertical output (default: horizontal output)')
    parser.add_argument('--keep-identical-mtune', action='store_true',
                        help='keep implied -mtune=...'
                             ' despite architecture identical to -march=... '
                        '(default: stripped away)')
    parser.add_argument('--keep-mno-flags', action='store_true',
                        help='keep -mno-* parameters (default: (superfluous ones) stripped away)')
    parser.add_argument('--keep-default-params', action='store_true',
                        help='keep --param ... with values matching defaults'
                             ' (default: stripped away)')
    parser.add_argument('--add-recommended', '-a', action='store_true',
                        help='add recommended flags (default: not added)')
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + VERSION_STR)
    options = parser.parse_args()

    try:
        native_unrolled_flag_set = Engine(
            options.gcc, options.debug).run(options)
    except Exception as e:
        if options.debug:
            traceback.print_exc()
        print('ERROR: %s' % str(e), file=sys.stderr)
        sys.exit(1)

    if options.add_recommended:
        add_recommended_flags(native_unrolled_flag_set)

    if options.formatting == _VERTICAL:
        joiner = '\n'
    else:
        joiner = ' '
    print(joiner.join(sorted(native_unrolled_flag_set, key=flags_sort_key)))


def main():
    try:
        _inner_main()
    except KeyboardInterrupt:
        sys.exit(128 + signal.SIGINT)


if __name__ == '__main__':
    main()
