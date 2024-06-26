#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

#end_pymotw_header
import textwrap
from textwrap_example import sample_text

# add the repr() to return a string containing a printable representation of an object
print(repr(sample_text))
print(textwrap.fill(sample_text, width=50))
