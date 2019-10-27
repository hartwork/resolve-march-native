# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

from __future__ import print_function

import sys

from resolve_march_native.parser import extract_flags
from resolve_march_native.runner import run


class NoTunePresentError(Exception):
	pass


class Engine(object):
	def __init__(self, gcc_command, debug):
		self._gcc_command = gcc_command
		self._debug = debug

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
		raise NoTunePresentError('No entry -tune=.. found in: %s' % ' '.join(sorted(flags)))

	@staticmethod
	def _dump_flags(flags):
		print('Flags extracted: %s' % ' '.join(sorted(flags)), file=sys.stderr)

	def _resolve_mtune(self, flag_set, arch):
		try:
			flag, tune = self._extract_tune_from_flags(flag_set)
			if tune == arch:
				flag_set.remove(flag)
		except NoTunePresentError:
		    pass

	@staticmethod
	def _resolve_mno_flags(flag_set):
		for flag in list(flag_set):
			if flag.startswith('-mno-'):
				flag_set.remove(flag)

	def _resolve_default_params(self, flag_set):
		defaults = {
			'l1-cache-line-size': 32,
			'l1-cache-size': 64,
			'l2-cache-size': 512,
		}
		needle_set = set(('--param %s=%s' % (k, v) for k, v in defaults.items()))

		for flag in list(flag_set):
			if flag in needle_set:
				if self._debug:
					print('Stripping %s because it is repeating defaults, only.' % flag, file=sys.stderr)
				flag_set.remove(flag)

	def _get_march_native_flag_set(self):
		march_native_flag_set = set(extract_flags(run(self._gcc_command, ['-march=native'], self._debug)))
		if self._debug:
			self._dump_flags(march_native_flag_set)
		return march_native_flag_set

	def _get_march_explicit_flag_set(self, march_explicit):
		march_explicit_flag_set = set(extract_flags(run(self._gcc_command, [march_explicit], self._debug)))
		if self._debug:
			self._dump_flags(march_explicit_flag_set)
		return march_explicit_flag_set

	@staticmethod
	def _get_march_explicit(arch):
		return '-march=%s' % arch

	def _process_flags_explicit_has_more(self, target_set, march_native_flag_set, march_explicit_flag_set):
		PREFIX_NO = '-mno-'
		PREFIX_YES = '-m'

		explicit_more_flag_set = march_explicit_flag_set - march_native_flag_set
		for flag in explicit_more_flag_set:
			if not flag.startswith('-m'):
				print('Unsure what to do about flag %s, please report this as a bug.' % flag, file=sys.stderr)
				continue

			if not flag.startswith(PREFIX_NO) and flag.startswith(PREFIX_YES):
				# march=<explicit> enabled something (too much) that march=native disabled
				opposite_flag = PREFIX_NO + flag[len(PREFIX_YES):]
				target_set.add(opposite_flag)

	def _resolve(self, march_native_flag_set, march_explicit_flag_set, arch, options):
		native_unrolled_flag_set = march_native_flag_set - march_explicit_flag_set
		native_unrolled_flag_set.add(self._get_march_explicit(arch))

		if not options.keep_identical_mtune:
			self._resolve_mtune(native_unrolled_flag_set, arch)
		if not options.keep_mno_flags:
			self._resolve_mno_flags(native_unrolled_flag_set)
		if not options.keep_default_params:
			self._resolve_default_params(native_unrolled_flag_set)

		# NOTE: The next step needs to go after resolution of -mno-* flags
		#       since it may add new -mno-* flags
		self._process_flags_explicit_has_more(native_unrolled_flag_set,
				march_native_flag_set, march_explicit_flag_set)

		return native_unrolled_flag_set

	def run(self, options):
		march_native_flag_set = self._get_march_native_flag_set()
		arch = self._extract_arch_from_flags(march_native_flag_set)
		march_explicit_flag_set = self._get_march_explicit_flag_set(
				self._get_march_explicit(arch))

		return self._resolve(march_native_flag_set, march_explicit_flag_set, arch, options)
