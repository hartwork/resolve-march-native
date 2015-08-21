#! /usr/bin/env make
# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

DESTDIR = /
PREFIX = /usr/local

check:
	py.test --doctest-modules

clean:
	find -type f -name '*.pyc' -delete

dist:
	$(RM) MANIFEST
	./setup.py sdist

install:
	./setup.py install --root "$(DESTDIR)" --prefix "$(PREFIX)"

.PHONY: check clean dist install
