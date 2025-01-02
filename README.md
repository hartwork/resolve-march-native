[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Run the test suite](https://github.com/hartwork/resolve-march-native/actions/workflows/run-tests.yml/badge.svg)](https://github.com/hartwork/resolve-march-native/actions/workflows/run-tests.yml)


# About

**resolve-march-native** is a small command line tool to resolve
`-march=native` into explicit GCC or Clang flags.


# Example

```console
$ resolve-march-native --vertical
-march=sandybridge
-maes
--param=l1-cache-line-size=64
--param=l1-cache-size=32
--param=l2-cache-size=3072
```

```console
$ resolve-march-native --clang --vertical
-target-cpu sandybridge
-target-feature +64bit
-target-feature +aes
-target-feature +avx
-target-feature +cmov
-target-feature +crc32
-target-feature +cx16
-target-feature +cx8
-target-feature +fxsr
-target-feature +mmx
-target-feature +pclmul
-target-feature +popcnt
-target-feature +sahf
-target-feature +sse
-target-feature +sse2
-target-feature +sse3
-target-feature +sse4.1
-target-feature +sse4.2
-target-feature +ssse3
-target-feature +xsave
-target-feature +xsaveopt
```

# Usage

```console
$ COLUMNS=80 resolve-march-native --help
usage: resolve-march-native [-h] [--debug] [--clang [COMMAND] | --gcc
                            [COMMAND]] [--vertical] [--keep-minus-features]
                            [--keep-identical-mtune] [--keep-mno-flags]
                            [--add-recommended] [--version]

options:
  -h, --help            show this help message and exit
  --debug               enable debugging (default: disabled)
  --clang [COMMAND]     target Clang (default: target GCC) and use given
                        command if any (default: clang)
  --gcc [COMMAND]       target GCC explicitly and use given command if any
                        (default: gcc))
  --vertical            produce vertical output (default: horizontal output)
  --add-recommended, -a
                        add recommended flags (default: not added)
  --version             show program's version number and exit

Clang-related arguments:
  --keep-minus-features
                        keep "-target-feature -*" style parameters (default:
                        stripped away)

GCC-related arguments:
  --keep-identical-mtune
                        keep implied -mtune=... despite architecture identical
                        to -march=... (default: stripped away)
  --keep-mno-flags      keep -mno-* parameters (default: (superfluous ones)
                        stripped away)

Software libre licensed under GPL v2 or later.
Brought to you by Sebastian Pipping <sebastian@pipping.org>.

Please report bugs at https://github.com/hartwork/resolve-march-native/issues — thank you!
```
