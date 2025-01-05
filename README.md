[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Run the test suite](https://github.com/hartwork/resolve-march-native/actions/workflows/run-tests.yml/badge.svg)](https://github.com/hartwork/resolve-march-native/actions/workflows/run-tests.yml)
[![Packaging status](https://repology.org/badge/tiny-repos/resolve-march-native.svg)](https://repology.org/project/resolve-march-native/versions)


# About

**resolve-march-native** is a small command line tool to resolve
`-march=native` into explicit GCC or (experimental!) Clang flags.


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
-march=sandybridge
-Xclang -target-feature -Xclang +64bit
-Xclang -target-feature -Xclang +aes
-Xclang -target-feature -Xclang +avx
-Xclang -target-feature -Xclang +cmov
-Xclang -target-feature -Xclang +crc32
-Xclang -target-feature -Xclang +cx16
-Xclang -target-feature -Xclang +cx8
-Xclang -target-feature -Xclang +fxsr
-Xclang -target-feature -Xclang +mmx
-Xclang -target-feature -Xclang +pclmul
-Xclang -target-feature -Xclang +popcnt
-Xclang -target-feature -Xclang +sahf
-Xclang -target-feature -Xclang +sse
-Xclang -target-feature -Xclang +sse2
-Xclang -target-feature -Xclang +sse3
-Xclang -target-feature -Xclang +sse4.1
-Xclang -target-feature -Xclang +sse4.2
-Xclang -target-feature -Xclang +ssse3
-Xclang -target-feature -Xclang +xsave
-Xclang -target-feature -Xclang +xsaveopt
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
  --clang [COMMAND]     [EXPERIMENTAL] target Clang (default: target GCC) and
                        use given command if any (default: clang)
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
