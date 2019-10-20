# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

import os
from unittest import TestCase

from resolve_march_native.parser import extract_flags
from resolve_march_native.engine import Engine


class TestEngine(TestCase):
	def _test_engine(self, expected_flag_set, basename_native, basename_explicit):
		data_home = 'resolve_march_native/test/data'

		with open(os.path.join(data_home, basename_native), 'r') as f:
			march_native_flag_set = set(extract_flags(f.read()))

		with open(os.path.join(data_home, basename_explicit), 'r') as f:
			march_explicit_flag_set = set(extract_flags(f.read()))

		class TestOptions(object):
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

	def test_bonnell(self):
		expected_flag_set = set((
			'--param l1-cache-size=24',
			'--param l1-cache-line-size=64',
			'-march=bonnell',
			'-mno-cx16',
		))

		self._test_engine(
				expected_flag_set,
				'bonnell--4-9-3-gentoo--native.s',
				'bonnell--4-9-3-gentoo--explicit.s',
				)

	def test_corei7_avx(self):
		expected_flag_set = set((
			'--param l1-cache-line-size=64',
			'--param l1-cache-size=32',
			'--param l2-cache-size=3072',
			'-march=corei7-avx',
		))

		self._test_engine(
				expected_flag_set,
				'corei7-avx--4-7-2-debian-wheezy--native.s',
				'corei7-avx--4-7-2-debian-wheezy--explicit.s',
				)

	def test_westmere(self):
		expected_flag_set = set((
			'--param l1-cache-line-size=64',
			'--param l1-cache-size=32',
			'--param l2-cache-size=12288',
			'-march=westmere',
		))

		self._test_engine(
				expected_flag_set,
				'westmere--4-9-3-gentoo--native.s',
				'westmere--4-9-3-gentoo--explicit.s',
				)
