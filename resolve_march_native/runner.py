# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

import os
import subprocess
import sys
import tempfile

from .environment import enforce_c_locale


def _fix_flags(flags):
    prefix = '--param '
    for flag in flags:
        if flag.startswith(prefix):
            yield '--param'
            yield flag[len(prefix):]
        else:
            yield flag


def run(gcc_command, flags, debug):
    tempdir = tempfile.mkdtemp()
    try:
        input_filename = os.path.join(tempdir, 'empty.c')
        open(input_filename, 'w')

        try:
            cmd = [
                gcc_command,
                '-S', '-fverbose-asm',
                '-o', '/dev/stdout',
                input_filename,
            ] + list(_fix_flags(flags))
            env = os.environ.copy()
            stderr = subprocess.DEVNULL
            enforce_c_locale(env)

            if debug:
                print('# %s' % ' '.join(cmd), file=sys.stderr)
                stderr = None  # i.e. forward to terminal

            try:
                return subprocess.check_output(cmd, env=env, stderr=stderr).decode('UTF-8')
            except OSError as e:
                e.strerror += ': "%s"' % gcc_command
                raise
        finally:
            os.remove(input_filename)
    finally:
        os.rmdir(tempdir)
