# data-processors
=======

[![Build Status](https://travis-ci.org/pkonarzewski/data-processors.svg?branch=master)](https://travis-ci.org/pkonarzewski/data-processors)
[![codecov](https://codecov.io/gh/pkonarzewski/data-processors/branch/master/graph/badge.svg)](https://codecov.io/gh/pkonarzewski/data-processors)

Data processing library based on pandas and numpy. It's goal is to be
collection of useful functions to process pandas series with efficient
and easy to use.

### Rules of library
1. Always use vectorised operations for efficiency
1. Input params should be Series, also sclars that are broadcasted
1. Output should Series
1. Output always have same length as input
1. Errors are silent and are returned as nulls
1. Processing funcs assume that data is in correct format, its user responsibility to keep them in correct format, although many modules have func to unify data [usually named: 'unify'].
