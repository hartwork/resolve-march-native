# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

from importlib.resources import files
from unittest import TestCase
from unittest.mock import patch

from resolve_march_native._gcc.engine import Engine
from resolve_march_native._gcc.parser import extract_flags


class TestEngine(TestCase):
    def _test_engine(self, expected_flag_set, basename_native, basename_explicit):
        with open(files('resolve_march_native._gcc.test') / 'data' / basename_native) as f:
            march_native_flag_set = set(extract_flags(f.read()))

        with open(files('resolve_march_native._gcc.test') / 'data' / basename_explicit) as f:
            march_explicit_flag_set = set(extract_flags(f.read()))

        class TestOptions:
            def __init__(self):
                self.gcc = 'gcc'
                self.debug = False
                self.keep_identical_mtune = False
                self.keep_mno_flags = False
                self.keep_default_params = False

        class TestEngine(Engine):
            def _get_march_native_flag_set(self, *_):
                return march_native_flag_set

            def _get_march_explicit_flag_set(self, *_):
                return march_explicit_flag_set

        options = TestOptions()
        engine = TestEngine(options.gcc, options.debug)
        received_flag_set = engine.run(options)

        self.assertEqual(received_flag_set, expected_flag_set)

    def test_armv8_a_crc(self):
        expected_flag_set = {
            '-march=armv8-a+crc',
        }

        self._test_engine(
            expected_flag_set,
            'armv8-a+crc--9-3-0-gentoo--native.s',
            'armv8-a+crc--9-3-0-gentoo--explicit.s',
        )

    def test_bonnell(self):
        expected_flag_set = {
            '--param l1-cache-size=24',
            '--param l1-cache-line-size=64',
            '--param l2-cache-size=512',
            '-march=bonnell',
            '-mno-cx16',
        }

        self._test_engine(
            expected_flag_set,
            'bonnell--4-9-3-gentoo--native.s',
            'bonnell--4-9-3-gentoo--explicit.s',
        )

    def test_corei7_avx(self):
        expected_flag_set = {
            '--param l1-cache-line-size=64',
            '--param l1-cache-size=32',
            '--param l2-cache-size=3072',
            '-march=corei7-avx',
        }

        self._test_engine(
            expected_flag_set,
            'corei7-avx--4-7-2-debian-wheezy--native.s',
            'corei7-avx--4-7-2-debian-wheezy--explicit.s',
        )

    def test_westmere(self):
        expected_flag_set = {
            '--param l1-cache-line-size=64',
            '--param l1-cache-size=32',
            '--param l2-cache-size=12288',
            '-march=westmere',
        }

        self._test_engine(
            expected_flag_set,
            'westmere--4-9-3-gentoo--native.s',
            'westmere--4-9-3-gentoo--explicit.s',
        )

    def test_sandybridge_celeron_without_avx(self):
        # NOTE: -mno-avx was cut away here by:
        #       1. keep_mno_flags = False
        #       2. ignorance of target help output
        expected_flag_set = {
            '-mmmx',
            '-mpopcnt',
            '-msse',
            '-msse2',
            '-msse3',
            '-mssse3',
            '-msse4.1',
            '-msse4.2',
            '-mpclmul',
            '-mcx16',
            '-mfxsr',
            '-msahf',
            '-mxsave',
            '-mxsaveopt',
            '--param=l1-cache-size=32',
            '--param=l1-cache-line-size=64',
            '--param=l2-cache-size=2048',
            '-march=sandybridge',
        }

        self._test_engine(
            expected_flag_set,
            'sandybridge-celeron--assembly-native.txt',
            'sandybridge-celeron--assembly-explicit.txt',
        )


class TestEngineFourFiles(TestCase):
    def _test_engine(self, expected_flag_set,
                     basename_assembly_native, basename_assembly_explicit,
                     basename_target_help_native, basename_target_help_explicit):
        def fake_subproces_check_output(args, *_1, **_2):
            if '-fverbose-asm' in args:
                if '-march=native' in args:
                    basename = basename_assembly_native
                else:
                    basename = basename_assembly_explicit
            else:
                assert '--help=target' in args
                if '-march=native' in args:
                    basename = basename_target_help_native
                else:
                    basename = basename_target_help_explicit

            filename = files('resolve_march_native._gcc.test') / 'data' / basename

            with open(filename, 'br') as f:
                return f.read()

        class TestOptions:
            def __init__(self):
                self.gcc = 'false'
                self.debug = False
                self.keep_identical_mtune = False
                self.keep_mno_flags = False
                self.keep_default_params = False

        options = TestOptions()
        engine = Engine(options.gcc, options.debug)

        with patch('subprocess.check_output', fake_subproces_check_output):
            received_flag_set = engine.run(options)

        self.assertEqual(received_flag_set, expected_flag_set)

    def test_sandybridge_celeron_without_avx(self):  # i.e. issue #110
        expected_flag_set = {
            '-mno-avx',
            '--param=l1-cache-line-size=64',
            '--param=l1-cache-size=32',
            '--param=l2-cache-size=2048',
            '-march=sandybridge',
        }

        self._test_engine(
            expected_flag_set,
            'sandybridge-celeron--assembly-native.txt',
            'sandybridge-celeron--assembly-explicit.txt',
            'sandybridge-celeron--target-help--native.txt',
            'sandybridge-celeron--target-help--explicit.txt',
        )

    def test_amd_k8_hammer(self):
        expected_flag_set = {
            '-mcx16',
            '-mprfchw',
            '-msahf',
            '--param=l1-cache-line-size=64',
            '--param=l1-cache-size=64',
            '--param=l2-cache-size=512',
            '-march=k8-sse3',
            '-mtune=k8',
        }

        self._test_engine(
            expected_flag_set,
            'amd-k8--assembly--native.txt',
            'amd-k8--assembly--explicit.txt',
            'amd-k8--target-help--native.txt',
            'amd-k8--target-help--explicit.txt',
        )

    def test_cfarm110_power7(self):
        expected_flag_set = {
            '-mcpu=power7',
        }

        self._test_engine(
            expected_flag_set,
            'cfarm110-power7--assembly--native.txt',
            'cfarm110-power7--assembly--explicit.txt',
            'cfarm110-power7--target-help--native.txt',
            'cfarm110-power7--target-help--explicit.txt',
        )

    def test_cfarm112_power8(self):
        expected_flag_set = {
            '-mcpu=power8',
        }

        self._test_engine(
            expected_flag_set,
            'cfarm112-power8--assembly--native.txt',
            'cfarm112-power8--assembly--explicit.txt',
            'cfarm112-power8--target-help--native.txt',
            'cfarm112-power8--target-help--explicit.txt',
        )

    def test_cfarm117_armv8_a_crypto_crc(self):
        expected_flag_set = {
            '-march=armv8-a+crypto+crc',
        }

        self._test_engine(
            expected_flag_set,
            'cfarm117-armv8-a+crypto+crc--assembly--native.txt',
            'cfarm117-armv8-a+crypto+crc--assembly--explicit.txt',
            'cfarm117-armv8-a+crypto+crc--target-help--native.txt',
            'cfarm117-armv8-a+crypto+crc--target-help--explicit.txt',
        )

    def test_cfarm118_armv8_a_crypto_crc(self):
        expected_flag_set = {
            '-march=armv8-a+crypto+crc',
        }

        self._test_engine(
            expected_flag_set,
            'cfarm118-armv8-a+crypto+crc--assembly--native.txt',
            'cfarm118-armv8-a+crypto+crc--assembly--explicit.txt',
            'cfarm118-armv8-a+crypto+crc--target-help--native.txt',
            'cfarm118-armv8-a+crypto+crc--target-help--explicit.txt',
        )

    def test_cfarm120_power10(self):
        expected_flag_set = {
            '-mcpu=power10',
        }

        self._test_engine(
            expected_flag_set,
            'cfarm120-power10--assembly--native.txt',
            'cfarm120-power10--assembly--explicit.txt',
            'cfarm120-power10--target-help--native.txt',
            'cfarm120-power10--target-help--explicit.txt',
        )

    def test_cfarm13_haswell(self):
        expected_flag_set = {
            '-mabm',
            '-maes',
            '--param=l1-cache-line-size=64',
            '--param=l1-cache-size=32',
            '--param=l2-cache-size=15360',
            '-march=haswell',
        }

        self._test_engine(
            expected_flag_set,
            'cfarm13-haswell--assembly--native.txt',
            'cfarm13-haswell--assembly--explicit.txt',
            'cfarm13-haswell--target-help--native.txt',
            'cfarm13-haswell--target-help--explicit.txt',
        )

    def test_cfarm14_haswell(self):
        expected_flag_set = {
            '-mabm',
            '-maes',
            '--param=l1-cache-line-size=64',
            '--param=l1-cache-size=32',
            '--param=l2-cache-size=15360',
            '-march=haswell',
        }

        self._test_engine(
            expected_flag_set,
            'cfarm14-haswell--assembly--native.txt',
            'cfarm14-haswell--assembly--explicit.txt',
            'cfarm14-haswell--target-help--native.txt',
            'cfarm14-haswell--target-help--explicit.txt',
        )

    def test_cfarm185_armv8_a_crypto_crc(self):
        expected_flag_set = {
            '-march=armv8-a+crypto+crc',
        }

        self._test_engine(
            expected_flag_set,
            'cfarm185-armv8-a+crypto+crc--assembly--native.txt',
            'cfarm185-armv8-a+crypto+crc--assembly--explicit.txt',
            'cfarm185-armv8-a+crypto+crc--target-help--native.txt',
            'cfarm185-armv8-a+crypto+crc--target-help--explicit.txt',
        )

    def test_cfarm186_westmere(self):
        expected_flag_set = {
            '-maes',
            '--param=l1-cache-line-size=64',
            '--param=l1-cache-size=32',
            '--param=l2-cache-size=12288',
            '-march=westmere',
        }

        self._test_engine(
            expected_flag_set,
            'cfarm186-westmere--assembly--native.txt',
            'cfarm186-westmere--assembly--explicit.txt',
            'cfarm186-westmere--target-help--native.txt',
            'cfarm186-westmere--target-help--explicit.txt',
        )

    def test_cfarm187_westmere(self):
        expected_flag_set = {
            '--param l1-cache-line-size=64',
            '--param l1-cache-size=32',
            '--param l2-cache-size=12288',
            '-march=westmere',
        }

        self._test_engine(
            expected_flag_set,
            'cfarm187-westmere--assembly--native.txt',
            'cfarm187-westmere--assembly--explicit.txt',
            'cfarm187-westmere--target-help--native.txt',
            'cfarm187-westmere--target-help--explicit.txt',
        )

    def test_cfarm188_westmere(self):
        expected_flag_set = {
            '--param l1-cache-line-size=64',
            '--param l1-cache-size=32',
            '--param l2-cache-size=12288',
            '-march=westmere',
        }

        self._test_engine(
            expected_flag_set,
            'cfarm188-westmere--assembly--native.txt',
            'cfarm188-westmere--assembly--explicit.txt',
            'cfarm188-westmere--target-help--native.txt',
            'cfarm188-westmere--target-help--explicit.txt',
        )

    def test_cfarm230_octeon2(self):
        expected_flag_set = {
            '-march=octeon2',
        }

        self._test_engine(
            expected_flag_set,
            'cfarm230-octeon2--assembly--native.txt',
            'cfarm230-octeon2--assembly--explicit.txt',
            'cfarm230-octeon2--target-help--native.txt',
            'cfarm230-octeon2--target-help--explicit.txt',
        )

    def test_cfarm29_power9(self):
        expected_flag_set = {
            '-mcpu=power9',
        }

        self._test_engine(
            expected_flag_set,
            'cfarm29-power9--assembly--native.txt',
            'cfarm29-power9--assembly--explicit.txt',
            'cfarm29-power9--target-help--native.txt',
            'cfarm29-power9--target-help--explicit.txt',
        )

    def test_cfarm70_nocona(self):
        expected_flag_set = {
            '-msahf',
            '--param l1-cache-line-size=64',
            '--param l1-cache-size=16',
            '--param l2-cache-size=2048',
            '-march=nocona',
        }

        self._test_engine(
            expected_flag_set,
            'cfarm70-nocona--assembly--native.txt',
            'cfarm70-nocona--assembly--explicit.txt',
            'cfarm70-nocona--target-help--native.txt',
            'cfarm70-nocona--target-help--explicit.txt',
        )

    def test_pentium(self):
        expected_flag_set = {
            '-mbranch-cost=3',
            '-mno-accumulate-outgoing-args',
            '-mno-sahf',
            '--param=l1-cache-line-size=64',
            '--param=l1-cache-size=32',
            '--param=l2-cache-size=1024',
            '-march=pentium-m',
            '-mtune=generic',
        }

        self._test_engine(
            expected_flag_set,
            'pentium-m--assembly--native.txt',
            'pentium-m--assembly--explicit.txt',
            'pentium-m--target-help--native.txt',
            'pentium-m--target-help--explicit.txt',
        )

    def test_sse4_weirdness_issue_177(self):
        expected_flag_set = {
            # No "-msse4" here!
            '-msse4.1',
            '-mxsave',
            '--param=l1-cache-size=32',
            '--param=l1-cache-line-size=64',
            '--param=l2-cache-size=6144',
            '-march=core2',
        }

        self._test_engine(
            expected_flag_set,
            'harpertown-core2--assembly--native.txt',
            'harpertown-core2--assembly--explicit.txt',
            'harpertown-core2--target-help--native.txt',
            'harpertown-core2--target-help--explicit.txt',
        )
