# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

_RECOMMENDED_FLAGS = (
        '-O2',
        '-pipe',
        )


def add_recommended_flags(flag_set):
    for flag in _RECOMMENDED_FLAGS:
        flag_set.add(flag)
