# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

import os
import subprocess
import tempfile

from resolve_march_native.environment import enforce_c_locale
from resolve_march_native.messenger import announce_command


def _fix_flags(flags):
    prefix = '--param '
    for flag in flags:
        if flag.startswith(prefix):
            yield '--param'
            yield flag[len(prefix):]
        else:
            yield flag


def run(gcc_command, flags, debug):
    with tempfile.NamedTemporaryFile(suffix='.c') as f:
        cmd = [
            gcc_command,
            '-S', '-fverbose-asm',
            '-o', '/dev/stdout',
            f.name,
        ] + list(_fix_flags(flags))
        env = os.environ.copy()
        stderr = subprocess.DEVNULL
        enforce_c_locale(env)

        if debug:
            announce_command(cmd)
            stderr = None  # i.e. forward to terminal

        try:
            return subprocess.check_output(cmd, env=env, stderr=stderr).decode('UTF-8')
        except OSError as e:
            e.strerror += ': "%s"' % gcc_command
            raise
