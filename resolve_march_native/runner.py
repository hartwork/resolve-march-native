# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

from __future__ import print_function

import os
import subprocess
import sys
import tempfile


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
        with open(input_filename, 'w') as f:
            pass

        try:
            output_filename = os.path.join(tempdir, 'march_native.s')
            cmd = [
                    gcc_command,
                    '-S', '-fverbose-asm',
                    '-o', output_filename,
                    input_filename,
                    ] + list(_fix_flags(flags))
            env = os.environ.copy()
            env.update({
                'LC_ALL': 'C',
            })
            for key in ('LANG', 'LANGUAGE'):
                env.pop(key, None)

            if debug:
                print('# %s' % ' '.join(cmd), file=sys.stderr)

            try:
                subprocess.check_output(cmd, env=env)
            except OSError as e:
                e.strerror += ': "%s"' % gcc_command
                raise

            try:
                with open(output_filename, 'r') as f:
                    return f.read()
            finally:
                os.remove(output_filename)
        finally:
            os.remove(input_filename)
    finally:
        os.rmdir(tempdir)
