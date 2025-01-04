# Copyright (C) 2025 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

import sys
from typing import Iterable


def announce_command(argv: list[str]) -> None:
    print('# %s' % ' '.join(argv), file=sys.stderr)


def announce_flags(flags: Iterable[str]) -> None:
    print('Flags extracted: %s' % ' '.join(sorted(flags)), file=sys.stderr)
