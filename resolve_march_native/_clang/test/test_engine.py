# Copyright (C) 2025 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

from importlib.resources import files
from unittest import TestCase
from unittest.mock import Mock, patch

from resolve_march_native._clang.engine import Engine
from resolve_march_native._clang.parser import HashHashHashOutputParser


class EngineTest(TestCase):
    maxDiff = None

    def assert_flags_equal(self, basename_explicit: str,
                           basename_native: str,
                           expected_flags_without_minus_features: list[str],
                           expected_flags_all: list[str]):
        with open(files('resolve_march_native._clang.test')
                  / 'data'
                  / basename_native, "br") as f:
            march_native_flag_set = set(HashHashHashOutputParser(f.readlines()).extract_flags())

        with open(files('resolve_march_native._clang.test')
                  / 'data'
                  / basename_explicit, "br") as f:
            march_explicit_flag_set = set(HashHashHashOutputParser(f.readlines()).extract_flags())

        for keep_minus_features, expected_flags in (
                (False, expected_flags_without_minus_features),
                (True, expected_flags_all),
        ):
            engine = Engine(clang_command='clang', debug=False)
            options = Mock(keep_minus_features=keep_minus_features)
            with patch.object(engine, '_get_march_native_flag_set',
                              return_value=march_native_flag_set):
                with patch.object(engine, '_get_march_explicit_flag_set',
                                  return_value=march_explicit_flag_set):
                    actual_flags = engine.run(options)
                    self.assertEqual(sorted(actual_flags, key=str.lower), expected_flags)

    def test_sandybridge_clang_19(self):
        self.assert_flags_equal(
            'sandybridge--clang-19--explicit.txt',
            'sandybridge--clang-19--native.txt',
            [
                '-march=sandybridge',
                '-Xclang -target-feature -Xclang +64bit',
                '-Xclang -target-feature -Xclang +aes',
                '-Xclang -target-feature -Xclang +avx',
                '-Xclang -target-feature -Xclang +cmov',
                '-Xclang -target-feature -Xclang +crc32',
                '-Xclang -target-feature -Xclang +cx16',
                '-Xclang -target-feature -Xclang +cx8',
                '-Xclang -target-feature -Xclang +fxsr',
                '-Xclang -target-feature -Xclang +mmx',
                '-Xclang -target-feature -Xclang +pclmul',
                '-Xclang -target-feature -Xclang +popcnt',
                '-Xclang -target-feature -Xclang +sahf',
                '-Xclang -target-feature -Xclang +sse',
                '-Xclang -target-feature -Xclang +sse2',
                '-Xclang -target-feature -Xclang +sse3',
                '-Xclang -target-feature -Xclang +sse4.1',
                '-Xclang -target-feature -Xclang +sse4.2',
                '-Xclang -target-feature -Xclang +ssse3',
                '-Xclang -target-feature -Xclang +xsave',
                '-Xclang -target-feature -Xclang +xsaveopt',
            ],
            [
                '-march=sandybridge',
                '-Xclang -target-feature -Xclang +64bit',
                '-Xclang -target-feature -Xclang +aes',
                '-Xclang -target-feature -Xclang +avx',
                '-Xclang -target-feature -Xclang +cmov',
                '-Xclang -target-feature -Xclang +crc32',
                '-Xclang -target-feature -Xclang +cx16',
                '-Xclang -target-feature -Xclang +cx8',
                '-Xclang -target-feature -Xclang +fxsr',
                '-Xclang -target-feature -Xclang +mmx',
                '-Xclang -target-feature -Xclang +pclmul',
                '-Xclang -target-feature -Xclang +popcnt',
                '-Xclang -target-feature -Xclang +sahf',
                '-Xclang -target-feature -Xclang +sse',
                '-Xclang -target-feature -Xclang +sse2',
                '-Xclang -target-feature -Xclang +sse3',
                '-Xclang -target-feature -Xclang +sse4.1',
                '-Xclang -target-feature -Xclang +sse4.2',
                '-Xclang -target-feature -Xclang +ssse3',
                '-Xclang -target-feature -Xclang +xsave',
                '-Xclang -target-feature -Xclang +xsaveopt',
                '-Xclang -target-feature -Xclang -adx',
                '-Xclang -target-feature -Xclang -amx-bf16',
                '-Xclang -target-feature -Xclang -amx-complex',
                '-Xclang -target-feature -Xclang -amx-fp16',
                '-Xclang -target-feature -Xclang -amx-int8',
                '-Xclang -target-feature -Xclang -amx-tile',
                '-Xclang -target-feature -Xclang -avx10.1-256',
                '-Xclang -target-feature -Xclang -avx10.1-512',
                '-Xclang -target-feature -Xclang -avx2',
                '-Xclang -target-feature -Xclang -avx512bf16',
                '-Xclang -target-feature -Xclang -avx512bitalg',
                '-Xclang -target-feature -Xclang -avx512bw',
                '-Xclang -target-feature -Xclang -avx512cd',
                '-Xclang -target-feature -Xclang -avx512dq',
                '-Xclang -target-feature -Xclang -avx512f',
                '-Xclang -target-feature -Xclang -avx512fp16',
                '-Xclang -target-feature -Xclang -avx512ifma',
                '-Xclang -target-feature -Xclang -avx512vbmi',
                '-Xclang -target-feature -Xclang -avx512vbmi2',
                '-Xclang -target-feature -Xclang -avx512vl',
                '-Xclang -target-feature -Xclang -avx512vnni',
                '-Xclang -target-feature -Xclang -avx512vp2intersect',
                '-Xclang -target-feature -Xclang -avx512vpopcntdq',
                '-Xclang -target-feature -Xclang -avxifma',
                '-Xclang -target-feature -Xclang -avxneconvert',
                '-Xclang -target-feature -Xclang -avxvnni',
                '-Xclang -target-feature -Xclang -avxvnniint16',
                '-Xclang -target-feature -Xclang -avxvnniint8',
                '-Xclang -target-feature -Xclang -bmi',
                '-Xclang -target-feature -Xclang -bmi2',
                '-Xclang -target-feature -Xclang -ccmp',
                '-Xclang -target-feature -Xclang -cf',
                '-Xclang -target-feature -Xclang -cldemote',
                '-Xclang -target-feature -Xclang -clflushopt',
                '-Xclang -target-feature -Xclang -clwb',
                '-Xclang -target-feature -Xclang -clzero',
                '-Xclang -target-feature -Xclang -cmpccxadd',
                '-Xclang -target-feature -Xclang -egpr',
                '-Xclang -target-feature -Xclang -enqcmd',
                '-Xclang -target-feature -Xclang -f16c',
                '-Xclang -target-feature -Xclang -fma',
                '-Xclang -target-feature -Xclang -fma4',
                '-Xclang -target-feature -Xclang -fsgsbase',
                '-Xclang -target-feature -Xclang -gfni',
                '-Xclang -target-feature -Xclang -hreset',
                '-Xclang -target-feature -Xclang -invpcid',
                '-Xclang -target-feature -Xclang -kl',
                '-Xclang -target-feature -Xclang -lwp',
                '-Xclang -target-feature -Xclang -lzcnt',
                '-Xclang -target-feature -Xclang -movbe',
                '-Xclang -target-feature -Xclang -movdir64b',
                '-Xclang -target-feature -Xclang -movdiri',
                '-Xclang -target-feature -Xclang -mwaitx',
                '-Xclang -target-feature -Xclang -ndd',
                '-Xclang -target-feature -Xclang -pconfig',
                '-Xclang -target-feature -Xclang -pku',
                '-Xclang -target-feature -Xclang -ppx',
                '-Xclang -target-feature -Xclang -prefetchi',
                '-Xclang -target-feature -Xclang -prfchw',
                '-Xclang -target-feature -Xclang -ptwrite',
                '-Xclang -target-feature -Xclang -push2pop2',
                '-Xclang -target-feature -Xclang -raoint',
                '-Xclang -target-feature -Xclang -rdpid',
                '-Xclang -target-feature -Xclang -rdpru',
                '-Xclang -target-feature -Xclang -rdrnd',
                '-Xclang -target-feature -Xclang -rdseed',
                '-Xclang -target-feature -Xclang -rtm',
                '-Xclang -target-feature -Xclang -serialize',
                '-Xclang -target-feature -Xclang -sgx',
                '-Xclang -target-feature -Xclang -sha',
                '-Xclang -target-feature -Xclang -sha512',
                '-Xclang -target-feature -Xclang -shstk',
                '-Xclang -target-feature -Xclang -sm3',
                '-Xclang -target-feature -Xclang -sm4',
                '-Xclang -target-feature -Xclang -sse4a',
                '-Xclang -target-feature -Xclang -tbm',
                '-Xclang -target-feature -Xclang -tsxldtrk',
                '-Xclang -target-feature -Xclang -uintr',
                '-Xclang -target-feature -Xclang -usermsr',
                '-Xclang -target-feature -Xclang -vaes',
                '-Xclang -target-feature -Xclang -vpclmulqdq',
                '-Xclang -target-feature -Xclang -waitpkg',
                '-Xclang -target-feature -Xclang -wbnoinvd',
                '-Xclang -target-feature -Xclang -widekl',
                '-Xclang -target-feature -Xclang -xop',
                '-Xclang -target-feature -Xclang -xsavec',
                '-Xclang -target-feature -Xclang -xsaves',
            ])
