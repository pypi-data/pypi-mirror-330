![PyPI - Version](https://img.shields.io/pypi/v/pymatroh)
![PyPI - License](https://img.shields.io/pypi/l/pymatroh)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pymatroh)
[![Publish PyPi](https://github.com/IT-Administrators/pymatroh/actions/workflows/release.yaml/badge.svg?branch=main)](https://github.com/IT-Administrators/pymatroh/actions/workflows/release.yaml)
[![CI](https://github.com/IT-Administrators/pymatroh/actions/workflows/ci.yaml/badge.svg)](https://github.com/IT-Administrators/pymatroh/actions/workflows/ci.yaml)

# pymatroh

_With the pymatroh module you can create different kind of matrices for testing purposes._

## Table of contents

1. [Introduction](#introduction)
2. [Getting started](#getting-started)
    1. [Prerequisites](#prerequisites)
    2. [Installation](#installation)
3. [How to use](#how-to-use)
    1. [How to import](#how-to-import)
    2. [Using the module](#using-the-module)
    3. [Using the cli](#using-the-cli)
4. [Releasing](#releasing)
5. [License](/LICENSE)

## Introduction

The intention of this module is to create matrices of different kinds for testing purposes.

You can create only integer matrices, float or complex matrices. Mixing these values is currently not implemented.

## Getting started

### Prerequisites

- Python installed
- Operatingsystem: Linux or Windows, not tested on mac
- IDE like VS Code, if you want to contribute or change the code

### Installation

There are two ways to install this module depending on the way you work and the preinstalled modules:

1. ```pip install pymatroh```

2. ```python -m pip install pymatroh```

## How to use

### How to Import

You can import the module in two ways:

```python
import pymatroh
```

- This will import all functions. Even the ones that are not supposed to be used.

```python
from pymatroh import *
```

- This will import only the significant functions, meant for using.

### Using the module

Depending on the way you imported the module, the following examples look a bit different.

Example 1: Using ```import <modulename>```
```python
# Import module.
import pymatroh
# Create integer matrix with just one value.
im = pymatroh.Matrix(1,1)
print(im.create_int_matrix())  
```
Result:
```
[[53]]
```

Example 2: Using ```from <modulename> import <submodule/class>```
```python
# Import class matrix from pymatroh package.
from pymatroh import Matrix
# Create float matrix.
fm = Matrix(2,2)
print(fm.create_float_matrix())
```
Result:
```python
[[0.3476066056691818, 82.64139933693019], [55.6682714565969, 37.442624968338635]]
```
Example 3: Using parameter applyround.
```python
# Import class matrix from pymatroh package.
from pymatroh import Matrix
# Create float matrix.
fm = Matrix(2,2,applyround=True)
print(fm.create_float_matrix())
```
Result:
```python
[[16.466, 24.297], [50.782, 36.962]]
```


### Using the cli

With the cli interface you can create python matrices and use them in scripts or export them to file
to use it in other projects.

To show the help run the following command:

```python
python -m pymatroh -h
```
Result:
```
usage: __main__.py [-h] [-row ROW] [-col COLUMN] [-rnge RANGE] [-mtype MATRIXTYPE] [-round ROUND]

options:
  -h, --help            show this help message and exit

Matrix:
  -row ROW, --row ROW   Row count.
  -col COLUMN, --column COLUMN
                        Column count.
  -rnge RANGE, --range RANGE
                        Integer range. Default = 100.
  -mtype MATRIXTYPE, --matrixtype MATRIXTYPE
                        Type of matrix. You can specify int,float or complex.
  -round ROUND, --round ROUND
                        Rounds the result by 3 digits.
```
Using the module via cli:
```
python -m pymatroh --row 2 --col 1 --round True --matrixtype float
```
Result:
```
[[69.856], [30.491]]
```

## Releasing

Releases are published automatically when a tag is pushed to GitHub.

```Powershell
# Create release variable.
$Release = "x.x.x"
# Create commit.
git commit --allow-empty -m "Release $Release"
# Create tag.
git tag -a $Release -m "Version $Release"
# Push from original.
git push origin --tags
# Push from fork.
git push upstream --tags
```

## License

[MIT](./LICENSE)