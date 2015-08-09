# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

def flags_sort_key(text):
	if text.startswith('-march='):
		return (0, text)  # March goes first
	elif text.startswith('--param'):
		return (2, text)  # --param goes last
	else:
		return (1, text)
