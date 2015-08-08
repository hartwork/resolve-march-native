# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

from __future__ import print_function

import sys

from resolve_march_native.parser import extract_flags
from resolve_march_native.runner import run


class Engine(object):
	@staticmethod
	def _extract_arch_from_flags(flags):
		prefix = '-march='
		for flag in flags:
			if flag.startswith(prefix):
				return flag[len(prefix):]
		raise ValueError('No entry -march=.. found in: %s' % ' '.join(sorted(flags)))

	@staticmethod
	def _extract_tune_from_flags(flags):
		prefix = '-mtune='
		for flag in flags:
			if flag.startswith(prefix):
				return (flag, flag[len(prefix):])
		raise ValueError('No entry -tune=.. found in: %s' % ' '.join(sorted(flags)))

	@staticmethod
	def _dump_flags(flags):
		print('Flags extracted: %s' % ' '.join(sorted(flags)), file=sys.stderr)

	def _resolve_mtune(self, flag_set, arch):
		flag, tune = self._extract_tune_from_flags(flag_set)
		if tune == arch:
			flag_set.remove(flag)

	@staticmethod
	def _resolve_mno_flags(flag_set):
		for flag in list(flag_set):
			if flag.startswith('-mno-'):
				flag_set.remove(flag)

	@staticmethod
	def _resolve_default_params(flag_set, debug):
		defaults = {
			'l1-cache-line-size': 32,
			'l1-cache-size': 64,
			'l2-cache-size': 512,
		}
		needle_set = set(('--param %s=%s' % (k, v) for k, v in defaults.items()))

		for flag in list(flag_set):
			if flag in needle_set:
				if debug:
					print('Stripping %s because it is repeating defaults, only.' % flag, file=sys.stderr)
				flag_set.remove(flag)


	def _get_march_native_flag_set(self, gcc_command, debug):
		march_native_flag_set = set(extract_flags(run(gcc_command, ['-march=native'], debug)))
		if debug:
			self._dump_flags(march_native_flag_set)
		return march_native_flag_set

	def _get_march_explicit_flag_set(self, gcc_command, debug, march_explicit):
		march_explicit_flag_set = set(extract_flags(run(gcc_command, [march_explicit], debug)))
		if debug:
			self._dump_flags(march_explicit_flag_set)
		return march_explicit_flag_set

	def run(self, options):
		march_native_flag_set = self._get_march_native_flag_set(options.gcc, options.debug)
		arch = self._extract_arch_from_flags(march_native_flag_set)
		march_explicit = '-march=%s' % arch
		march_explicit_flag_set = self._get_march_explicit_flag_set(options.gcc, options.debug, march_explicit)

		native_unrolled_flag_set = march_native_flag_set - march_explicit_flag_set
		native_unrolled_flag_set.add(march_explicit)

		native_unrolled_flag_set_backup = native_unrolled_flag_set.copy()
		if not options.keep_identical_mtune:
			self._resolve_mtune(native_unrolled_flag_set, arch)
		if not options.keep_mno_flags:
			self._resolve_mno_flags(native_unrolled_flag_set)
		if not options.keep_default_params:
			self._resolve_default_params(native_unrolled_flag_set, options.debug)

		if set(extract_flags(run(options.gcc, native_unrolled_flag_set_backup, options.debug))) != march_native_flag_set:
			print('ERROR: Sanity checks failed, flag list may be mistaken', file=sys.stderr)
			sys.exit(1)

		return native_unrolled_flag_set
