#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handling and converting ISBN numbers.

Although International Standard Book Numbers have been issued as ISBN-13s for
some years, users still have to cope with a large number of legacy ISBN-10s.
This package provides functions for converting between ISBN types and
stripping ISBNs, encapsulating these in a simple class.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

from isbn import Isbn
from utils import *


### CONSTANTS & DEFINES ###

__version__ = '0.1'


### IMPLEMENTATION ###

### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
