# Copyright (C) 2025 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

import os
import subprocess

from resolve_march_native._clang.parser import HashHashHashOutputParser
from resolve_march_native.environment import enforce_c_locale


class Engine:
    def __init__(self, clang_command: str, debug: bool):
        self._clang_command = clang_command
        self._debug = debug

    def _extract_arch_from_flags(self, march_native_flag_set: set[str]) -> str:
        expected_prefix = '-target-cpu '
        return [f[len(expected_prefix):] for f in march_native_flag_set
                if f.startswith(expected_prefix)][-1]

    def _get_flag_set(self, extra_argv) -> set[str]:
        argv = [self._clang_command, '-E', *extra_argv, '-###', '-']
        env = os.environ.copy()
        enforce_c_locale(env)
        p = subprocess.run(argv,
                           stdin=subprocess.DEVNULL,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.PIPE,
                           env=env)
        p.check_returncode()
        return set(HashHashHashOutputParser(p.stderr.splitlines()).extract_flags())

    def _get_march_native_flag_set(self) -> set[str]:
        return self._get_flag_set(["-march=native"])

    def _get_march_explicit_flag_set(self, arch) -> set[str]:
        return self._get_flag_set([f"-march={arch}"])

    def _resolve(self, march_native_flag_set: set[str], march_explicit_flag_set: set[str],
                 arch: str, options) -> set[str]:
        reduced_set = march_native_flag_set - march_explicit_flag_set
        if not options.keep_minus_features:
            for minus_feature_arg in [a for a in reduced_set if a.startswith('-target-feature -')]:
                reduced_set.remove(minus_feature_arg)
        reduced_set.add(f'-target-cpu {arch}')
        return reduced_set

    def run(self, options) -> set[str]:
        march_native_flag_set = self._get_march_native_flag_set()
        arch = self._extract_arch_from_flags(march_native_flag_set)
        march_explicit_flag_set = self._get_march_explicit_flag_set(arch)
        return self._resolve(march_native_flag_set, march_explicit_flag_set, arch, options)