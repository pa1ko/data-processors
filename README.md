# data-processors

[![Build Status](https://travis-ci.org/pkonarzewski/data-processors.svg?branch=master)](https://travis-ci.org/pkonarzewski/data-processors)
[![codecov](https://codecov.io/gh/pkonarzewski/data-processors/branch/master/graph/badge.svg)](https://codecov.io/gh/pkonarzewski/data-processors)

Toy project to learn how to use pandas and numpy efficiently

### Rules of library
1. Always use vectorised operations for efficiency
1. Input params should be Series, also sclars that are broadcasted
1. Output should Series
1. Output always have same length as input
1. Errors are silent and are returned as nulls
1. Processing funcs assume that data is in correct format, its user responsibility to keep them in correct format, although many modules have func to unify data [usually named: 'unify'].
