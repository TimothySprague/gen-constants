# gen_constants

This package is intended to generate files from multiple languages for a set of constants and/or enumerations.

## Usage

Generate a C header and a Python file in the current working directory using the sample config:

```sh
$ python3 -m gen_constants --generate-c --generate-python ./sample.ini
```

See full help with:

```sh
$ python3 -m gen_constants -h
```