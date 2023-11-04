# Copyright (C) 2022 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

from unittest import TestCase
from unittest.mock import patch

from pkg_resources import resource_filename

from ..target_help_parser import _parse_gcc_output, get_flags_implied_by_march


class GetFlagsImpliedByMarchTest(TestCase):
    def test(self):
        stdout_mock_filename = resource_filename(
            'resolve_march_native.test',
            'data/sandybridge--11-3-0-gentoo--target-help.txt'
        )
        with open(stdout_mock_filename, 'rb') as f:
            stdout_mock_bytes = f.read()
        expected_flags = [
            '-m128bit-long-double',
            '-m64',
            '-m80387',
            '-mabi=sysv',
            '-maddress-mode=long',
            '-malign-data=compat',
            '-malign-functions=0',
            '-malign-jumps=0',
            '-malign-loops=0',
            '-malign-stringops',
            '-march=sandybridge',
            '-masm=att',
            '-mavx',
            '-mavx256-split-unaligned-load',
            '-mavx256-split-unaligned-store',
            '-mbranch-cost=3',
            '-mcpu=',
            '-mcrc32',
            '-mcx16',
            '-mfancy-math-387',
            '-mfentry-name=',
            '-mfentry-section=',
            '-mfp-ret-in-387',
            '-mfpmath=sse',
            '-mfunction-return=keep',
            '-ffp-contract=fast',
            '-mfxsr',
            '-mglibc',
            '-mhard-float',
            '-mharden-sls=none',
            '-mieee-fp',
            '-mincoming-stack-boundary=0',
            '-mindirect-branch=keep',
            '-minstrument-return=none',
            '-masm=intel',
            '-mlarge-data-threshold=65536',
            '-mlong-double-80',
            '-mmemcpy-strategy=',
            '-mmemset-strategy=',
            '-mmmx',
            '-mmwait',
            '-mpclmul',
            '-mpopcnt',
            '-mprefer-vector-width=128',
            '-mprefer-vector-width=none',
            '-mpreferred-stack-boundary=0',
            '-mpush-args',
            '-mrecip=',
            '-mred-zone',
            '-mregparm=6',
            '-msahf',
            '-msse',
            '-msse2',
            '-msse3',
            '-msse4',
            '-msse4.1',
            '-msse4.2',
            '-mavx',
            '-mssse3',
            '-mstack-protector-guard-offset=',
            '-mstack-protector-guard-reg=',
            '-mstack-protector-guard-symbol=',
            '-mstack-protector-guard=tls',
            '-mstv',
            '-mtls-dialect=gnu',
            '-mtls-direct-seg-refs',
            '-mtune-ctrl=',
            '-mtune=sandybridge',
            '-mvzeroupper',
            '-mxsave',
            '-mxsaveopt',
        ]
        with patch('subprocess.check_output', return_value=stdout_mock_bytes):
            actual_flags = get_flags_implied_by_march('sandybridge')
        self.assertEqual(actual_flags, expected_flags)

    def test_macos(self):
        stdout_mock_filename = resource_filename(
            'resolve_march_native.test',
            'data/native-ivybridge--10-4-0-macos-homebrew--target-help.txt'
        )
        with open(stdout_mock_filename, 'rb') as f:
            stdout_mock_bytes = f.read()
        expected_flags = [
            '-Wnonportable-cfstrings',
            '-m128bit-long-double',
            '-m64',
            '-m80387',
            '-mabi=sysv',
            '-maddress-mode=long',
            '-maes',
            '-malign-data=compat',
            '-malign-functions=0',
            '-malign-jumps=0',
            '-malign-loops=0',
            '-malign-stringops',
            '-march=ivybridge',
            '-masm=att',
            '-matt-stubs',
            '-mavx',
            '-mavx256-split-unaligned-load',
            '-mavx256-split-unaligned-store',
            '-mbranch-cost=3',
            '-mconstant-cfstrings',
            '-mcpu=',
            '-mcx16',
            '-mf16c',
            '-mfancy-math-387',
            '-mfentry-name=',
            '-mfentry-section=',
            '-mfp-ret-in-387',
            '-mfpmath=sse',
            '-mfsgsbase',
            '-mfunction-return=keep',
            '-ffp-contract=fast',
            '-mfxsr',
            '-mhard-float',
            '-mieee-fp',
            '-mincoming-stack-boundary=0',
            '-mindirect-branch=keep',
            '-minstrument-return=none',
            '-masm=intel',
            '-mlarge-data-threshold=65536',
            '-mlong-double-80',
            '-mmacosx-version-min=11.0.0',
            '-mmemcpy-strategy=',
            '-mmemset-strategy=',
            '-mmmx',
            '-mpclmul',
            '-mpopcnt',
            '-mprefer-vector-width=128',
            '-mprefer-vector-width=none',
            '-mpreferred-stack-boundary=0',
            '-mpush-args',
            '-mrdrnd',
            '-mrecip=',
            '-mred-zone',
            '-mregparm=6',
            '-msahf',
            '-msse',
            '-msse2',
            '-msse3',
            '-msse4',
            '-msse4.1',
            '-msse4.2',
            '-mavx',
            '-mssse3',
            '-mstack-protector-guard-offset=',
            '-mstack-protector-guard-reg=',
            '-mstack-protector-guard-symbol=',
            '-mstack-protector-guard=global',
            '-mstv',
            '-mtarget-linker 711',
            '-mtarget-linker=',
            '-mtls-dialect=gnu',
            '-mtune-ctrl=',
            '-mtune=ivybridge',
            '-mvzeroupper',
            '-mxsave'
        ]
        with patch('subprocess.check_output', return_value=stdout_mock_bytes):
            actual_flags = get_flags_implied_by_march('native')
        self.assertEqual(actual_flags, expected_flags)


class ParseGccOutputTest(TestCase):
    def test_deprecated_lines(self):
        self.assertEqual(_parse_gcc_output('  -mfused-madd                \t\t'), [])

    def test_ignore_lines(self):
        self.assertEqual(_parse_gcc_output('  -fapple-kext                \t\t[available in C++]'),
                         [])

    def test_equal_value_default_lines(self):
        # https://github.com/hartwork/resolve-march-native/issues/72
        self.assertEqual(_parse_gcc_output('  -mabi=ABI                   \t\tlp64'),
                         ['-mabi=lp64'])

    def test_value_default_lines(self):
        # On cfarm29 (ppc64le)
        self.assertEqual(_parse_gcc_output('  -G<number>                  \t\t8'),
                         ['-G8'])

    def test_concat_arg_lines(self):
        # On cfarm29 (ppc64le)
        self.assertEqual(_parse_gcc_output('  -malign-                    \t\tnatural'),
                         ['-malign-natural'])

    def test_concat_var_lines(self):
        # On cfarm29 (ppc64le)
        self.assertEqual(_parse_gcc_output('  -mcall-ABI                  \t\tlinux'),
                         ['-mcall-linux'])

    def test_ignore_marked_lines(self):
        # On cfarm29 (ppc64le)
        self.assertEqual(_parse_gcc_output('  -mgen-cell-microcode        \t\t[ignored]'),
                         ['-mgen-cell-microcode'])

    def test_array_value_lines(self):
        # On cfarm29 (ppc64le)
        self.assertEqual(_parse_gcc_output('  -msdata=[none,data,sysv,eabi] \tnone'),
                         ['-msdata=none'])
