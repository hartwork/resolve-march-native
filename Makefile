#! /usr/bin/env make
# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

check:
	py.test --doctest-modules

clean:
	find -type f -name '*.pyc' -delete

dist:
	$(RM) MANIFEST
	./setup.py sdist

.PHONY: check clean dist
