# Copyright (C) 2022 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

from unittest import TestCase
from unittest.mock import patch

from pkg_resources import resource_filename

from ..target_help_parser import get_flags_implied_by_march


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