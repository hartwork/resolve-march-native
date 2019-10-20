#! /usr/bin/env python
# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

from setuptools import setup

from resolve_march_native.version import VERSION_STR

def _read(filename):
    with open(filename, 'r') as f:
        return f.read()


if __name__ == '__main__':
    setup(
            name='resolve-march-native',
            description='Tool to determine what GCC flags -march=native would resolve into',
            long_description=_read('README.rst'),
            license='GPLv2+',
            version=VERSION_STR,
            author='Sebastian Pipping',
            author_email='sebastian@pipping.org',
            url='https://github.com/hartwork/resolve-march-native',
            packages=[
                'resolve_march_native',
            ],
            scripts=[
                'resolve-march-native',
            ],
            classifiers=[
                'Development Status :: 4 - Beta',
                'Environment :: Console',
                'Intended Audience :: End Users/Desktop',
                'Intended Audience :: System Administrators',
                'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
                'Natural Language :: English',
                'Operating System :: POSIX :: Linux',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.5',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7',
                'Topic :: Software Development :: Compilers',
                'Topic :: Utilities',
            ],
            )
