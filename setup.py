#! /usr/bin/env python
# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

from setuptools import setup

from resolve_march_native.version import VERSION_STR


def _read(filename):
    with open(filename) as f:
        return f.read()


if __name__ == '__main__':
    setup(
        name='resolve-march-native',
        description='Tool to determine what GCC flags -march=native would resolve into',
        long_description=_read('README.md'),
        long_description_content_type='text/markdown',
        license='GPLv2+',
        version=VERSION_STR,
        author='Sebastian Pipping',
        author_email='sebastian@pipping.org',
        url='https://github.com/hartwork/resolve-march-native',
        python_requires='>=3.8',
        setup_requires=[
            'setuptools>=38.6.0',  # for long_description_content_type
        ],
        packages=[
                'resolve_march_native',
        ],
        entry_points={
            'console_scripts': [
                'resolve-march-native = resolve_march_native.__main__:main',
            ],
        },
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Software Development :: Compilers',
            'Topic :: Utilities',
        ],
    )
