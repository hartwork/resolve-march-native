from importlib.resources import files
from unittest import TestCase
from unittest.mock import Mock, patch

from resolve_march_native._clang.engine import Engine
from resolve_march_native._clang.parser import HashHashHashOutputParser


class EngineTest(TestCase):
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
                    self.assertEqual(sorted(actual_flags), expected_flags)

    def test_sandybridge_clang_19(self):
        self.assert_flags_equal(
            'sandybridge--clang-19--explicit.txt',
            'sandybridge--clang-19--native.txt',
            [
                '-target-cpu sandybridge',
                '-target-feature +64bit',
                '-target-feature +aes',
                '-target-feature +avx',
                '-target-feature +cmov',
                '-target-feature +crc32',
                '-target-feature +cx16',
                '-target-feature +cx8',
                '-target-feature +fxsr',
                '-target-feature +mmx',
                '-target-feature +pclmul',
                '-target-feature +popcnt',
                '-target-feature +sahf',
                '-target-feature +sse',
                '-target-feature +sse2',
                '-target-feature +sse3',
                '-target-feature +sse4.1',
                '-target-feature +sse4.2',
                '-target-feature +ssse3',
                '-target-feature +xsave',
                '-target-feature +xsaveopt',
            ],
            [
                '-target-cpu sandybridge',
                '-target-feature +64bit',
                '-target-feature +aes',
                '-target-feature +avx',
                '-target-feature +cmov',
                '-target-feature +crc32',
                '-target-feature +cx16',
                '-target-feature +cx8',
                '-target-feature +fxsr',
                '-target-feature +mmx',
                '-target-feature +pclmul',
                '-target-feature +popcnt',
                '-target-feature +sahf',
                '-target-feature +sse',
                '-target-feature +sse2',
                '-target-feature +sse3',
                '-target-feature +sse4.1',
                '-target-feature +sse4.2',
                '-target-feature +ssse3',
                '-target-feature +xsave',
                '-target-feature +xsaveopt',
                '-target-feature -adx',
                '-target-feature -amx-bf16',
                '-target-feature -amx-complex',
                '-target-feature -amx-fp16',
                '-target-feature -amx-int8',
                '-target-feature -amx-tile',
                '-target-feature -avx10.1-256',
                '-target-feature -avx10.1-512',
                '-target-feature -avx2',
                '-target-feature -avx512bf16',
                '-target-feature -avx512bitalg',
                '-target-feature -avx512bw',
                '-target-feature -avx512cd',
                '-target-feature -avx512dq',
                '-target-feature -avx512f',
                '-target-feature -avx512fp16',
                '-target-feature -avx512ifma',
                '-target-feature -avx512vbmi',
                '-target-feature -avx512vbmi2',
                '-target-feature -avx512vl',
                '-target-feature -avx512vnni',
                '-target-feature -avx512vp2intersect',
                '-target-feature -avx512vpopcntdq',
                '-target-feature -avxifma',
                '-target-feature -avxneconvert',
                '-target-feature -avxvnni',
                '-target-feature -avxvnniint16',
                '-target-feature -avxvnniint8',
                '-target-feature -bmi',
                '-target-feature -bmi2',
                '-target-feature -ccmp',
                '-target-feature -cf',
                '-target-feature -cldemote',
                '-target-feature -clflushopt',
                '-target-feature -clwb',
                '-target-feature -clzero',
                '-target-feature -cmpccxadd',
                '-target-feature -egpr',
                '-target-feature -enqcmd',
                '-target-feature -f16c',
                '-target-feature -fma',
                '-target-feature -fma4',
                '-target-feature -fsgsbase',
                '-target-feature -gfni',
                '-target-feature -hreset',
                '-target-feature -invpcid',
                '-target-feature -kl',
                '-target-feature -lwp',
                '-target-feature -lzcnt',
                '-target-feature -movbe',
                '-target-feature -movdir64b',
                '-target-feature -movdiri',
                '-target-feature -mwaitx',
                '-target-feature -ndd',
                '-target-feature -pconfig',
                '-target-feature -pku',
                '-target-feature -ppx',
                '-target-feature -prefetchi',
                '-target-feature -prfchw',
                '-target-feature -ptwrite',
                '-target-feature -push2pop2',
                '-target-feature -raoint',
                '-target-feature -rdpid',
                '-target-feature -rdpru',
                '-target-feature -rdrnd',
                '-target-feature -rdseed',
                '-target-feature -rtm',
                '-target-feature -serialize',
                '-target-feature -sgx',
                '-target-feature -sha',
                '-target-feature -sha512',
                '-target-feature -shstk',
                '-target-feature -sm3',
                '-target-feature -sm4',
                '-target-feature -sse4a',
                '-target-feature -tbm',
                '-target-feature -tsxldtrk',
                '-target-feature -uintr',
                '-target-feature -usermsr',
                '-target-feature -vaes',
                '-target-feature -vpclmulqdq',
                '-target-feature -waitpkg',
                '-target-feature -wbnoinvd',
                '-target-feature -widekl',
                '-target-feature -xop',
                '-target-feature -xsavec',
                '-target-feature -xsaves',
            ])
