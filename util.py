#!/usr/bin/env python
##### UTIL
import operator

def product(iterable):
    return reduce(operator.mul, iterable, 1)