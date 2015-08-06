About
=====

`resolve-march-native` is a small command line tool to resolve
`-march=native` into explicit GCC flags.


Example
=======

```
$ resolve-march-native --vertical
--param l1-cache-line-size=64
--param l1-cache-size=32
--param l2-cache-size=3072
-march=corei7-avx
```


Usage
=====

```
$ resolve-march-native --help
usage: resolve-march-native [-h] [--debug] [--gcc COMMAND] [--vertical]
                            [--keep-identical-mtune] [--keep-mno-flags]
                            [--keep-default-params] [--version]

optional arguments:
  -h, --help            show this help message and exit
  --debug               enable debugging (default: disabled)
  --gcc COMMAND         gcc command (default: gcc)
  --vertical            produce vertical output (default: horizontal output)
  --keep-identical-mtune
                        keep implied -mtune=... despite architecture identical
                        to -march=... (default: stripped away)
  --keep-mno-flags      keep -mno-* paramters (default: stripped away)
  --keep-default-params
                        keep --param ... with values matching defaults
                        (default: stripped away)
  --version             show program's version number and exit

resolve-march-native is software libre licensed under GPL v2 or later,
written by Sebastian Pipping.  Please report bugs to
https://github.com/hartwork/resolve-march-native/issues.  Thanks!
```
