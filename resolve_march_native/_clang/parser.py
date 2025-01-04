# Copyright (C) 2025 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

import re
from typing import Generator

_SINGLE_PARAM_ARGS = {
    # NOTE: It's probably okay to be incomplete here, so far "-target-feature [+-]FEATURE"
    #       is the only thing that survives diffing...
    '-ferror-limit',
    '-include',
    '-internal-externc-isystem',
    '-internal-isystem',
    '-main-file-name',
    '-mrelocation-model',
    '-o',
    '-pic-level',
    '-resource-dir',
    '-stack-protector',
    '-target-cpu',
    '-target-feature',
    '-triple',
    '-x',
}


class HashHashHashOutputParser:
    def __init__(self, lines: list[str]):
        self._lines = lines
        self._matcher = re.compile(b'"(?P<arg>[^"]+)"')

    def _extract_raw_flags(self) -> Generator[str, None, None]:
        for line in self._lines:
            for match in re.finditer(self._matcher, line, 0):
                argument = match.group("arg").decode('utf-8')
                yield argument

    def extract_flags(self) -> Generator[str, None, None]:
        prev = None
        for arg in self._extract_raw_flags():
            if arg in _SINGLE_PARAM_ARGS:
                prev = arg
                continue

            if prev is not None:
                arg = f"{prev} {arg}"
                prev = None

            yield arg
