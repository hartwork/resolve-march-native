#! /usr/bin/env python3
# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

import argparse
import signal
import sys
import traceback
from textwrap import dedent

from resolve_march_native._clang.engine import Engine as ClangEngine
from resolve_march_native._gcc.engine import Engine as GccEngine

from .recommended import add_recommended_flags
from .sort import flags_sort_key
from .version import VERSION_STR

_HORIZONTAL, _VERTICAL = range(2)
_CLANG_COMMAND = "clang"
_GCC_COMMAND = "gcc"
_UNSET = object()


def _inner_main():
    parser = argparse.ArgumentParser(
        prog='resolve-march-native',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent("""\
                Software libre licensed under GPL v2 or later.
                Brought to you by Sebastian Pipping <sebastian@pipping.org>.

                Please report bugs at https://github.com/hartwork/resolve-march-native/issues — thank you!
                """),  # noqa: E501
    )
    parser.add_argument('--debug', action='store_true',
                        help='enable debugging (default: disabled)')

    clang_or_gcc = parser.add_mutually_exclusive_group()
    clang_or_gcc.add_argument('--clang', default=_UNSET, metavar='COMMAND', nargs='?',
                              help='[EXPERIMENTAL] target Clang (default: target GCC)'
                                   f' and use given command if any (default: {_CLANG_COMMAND})')
    clang_or_gcc.add_argument('--gcc', default=_UNSET, metavar='COMMAND', nargs='?',
                              help='target GCC explicitly'
                                   f' and use given command if any (default: {_GCC_COMMAND}))')

    parser.add_argument('--vertical', dest='formatting',
                        default=_HORIZONTAL, action='store_const', const=_VERTICAL,
                        help='produce vertical output (default: horizontal output)')

    clang_arguments = parser.add_argument_group(title="Clang-related arguments")
    clang_arguments.add_argument('--keep-minus-features', action='store_true',
                                 help='keep "-target-feature -*" style parameters'
                                      ' (default: stripped away)')

    gcc_arguments = parser.add_argument_group(title="GCC-related arguments")
    gcc_arguments.add_argument('--keep-identical-mtune', action='store_true',
                               help='keep implied -mtune=...'
                                    ' despite architecture identical to -march=... '
                                    '(default: stripped away)')
    gcc_arguments.add_argument('--keep-mno-flags', action='store_true',
                               help='keep -mno-* parameters'
                                    ' (default: (superfluous ones) stripped away)')

    parser.add_argument('--add-recommended', '-a', action='store_true',
                        help='add recommended flags (default: not added)')
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + VERSION_STR)
    options = parser.parse_args()

    try:
        if options.clang is not _UNSET:
            if options.clang is None:  # i.e. short "--clang" rather than "--clang COMMAND"
                options.clang = _CLANG_COMMAND
            native_unrolled_flag_set = ClangEngine(options.clang, options.debug).run(options)
        else:
            if options.gcc in (_UNSET, None):
                options.gcc = _GCC_COMMAND
            native_unrolled_flag_set = GccEngine(options.gcc, options.debug).run(options)
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
