# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

from unittest import TestCase

from resolve_march_native.sort import flags_sort_key


class TestSort(TestCase):
	def test_bonnell(self):
		input_order = [
			'--param l1-cache-size=24',
			'-march=bonnell',
			'-mno-cx16',
			'--param l1-cache-line-size=64',
		]
		expected_order = [
			'-march=bonnell',
			'-mno-cx16',
			'--param l1-cache-line-size=64',
			'--param l1-cache-size=24',
		]
		actual_order = sorted(input_order, key=flags_sort_key)
		self.assertEqual(actual_order, expected_order)
