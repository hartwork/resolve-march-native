#! /usr/bin/env make
# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

check:
	py.test --doctest-modules

.PHONY: check
