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
-mno-abm
-mno-avx2
-mno-bmi
-mno-bmi2
-mno-f16c
-mno-fma
-mno-fma4
-mno-fsgsbase
-mno-lwp
-mno-lzcnt
-mno-movbe
-mno-rdrnd
-mno-tbm
-mno-xop
-mtune=corei7-avx
```


Usage
=====

```
$ resolve-march-native --help
usage: resolve-march-native [-h] [--debug] [--gcc COMMAND] [--vertical]
                            [--version]

optional arguments:
  -h, --help     show this help message and exit
  --debug        enable debugging (default: disabled)
  --gcc COMMAND  gcc command (default: gcc)
  --vertical     produce vertical output (default: horizontal output)
  --version      show program's version number and exit

resolve-march-native is software libre licensed under GPL v2 or later,
written by Sebastian Pipping.  Please report bugs to
https://github.com/hartwork/resolve-march-native/issues.  Thanks!
```
