#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
A unified class for handling ISBNs.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import utils

__all__ = [
	'Isbn',
]

__version__ = '0.1b'


### IMPLEMENTATION ###

class Isbn (object):
	"""
	An ISBN number.
	
	This encapsulates most of the utility functions, supporting initialisation
	from any forms and interconversion. It can be set from an ISBN-13, ISBN-10
	or SBN and will return
	
	For example::
	
		>>> y = Isbn ("978-0940-01673-6")
		>>> y.isbn13
		'9780940016736'
		>>> y.isbn10
		'0940016737'
		>>> y.sbn
		'940016737'
		>>> y.asin
		'0940016737'
	
	"""
	def __init__ (self, isbn_str):
		"""
		Ctor, using a string representation of the ISBN.
		
		:Parameters:
			isbn_str : string
				A 10- or 13-digit form of the ISBN, or an old-style 9 digit SBN.
				Formatting (whitespace and hyphens) is allowed and is stripped out
				before use.
				
		For example::
		
				>>> x = Isbn ("3-8055-7505-X")
				>>> y = Isbn ("9780940016736")
				>>> z = Isbn ("940016737")
				
		"""
		# Main:
		clean_str = utils.clean_isbn (isbn_str)
		isbn_len = len (clean_str)
		if (isbn_len == 9):
			self.sbn = clean_str
		elif (isbn_len == 10):
			self.isbn10 = clean_str
		elif (isbn_len == 13):
			self.isbn13 = clean_str
		else:
			raise ValueError ("ISBN '%s' should be 9, 10 or 13 characters" %
				isbn_str)

	def __str__ (self):
		return "%s (%s)" % (self.__class__, self.isbn13)
	
	def __unicode__ (self):
		return unicode (self)
	
	### INTERNAL:
	def _get_isbn10 (self):
		return self._isbn10

	def _set_isbn10 (self, isbn_str):
		isbn_str = utils.clean_isbn (isbn_str)
		assert (len (isbn_str) == 10)
		self._isbn10 = isbn_str
		self._isbn13 = utils.isbn10_to_isbn13 (isbn_str)
		self._sbn = utils.isbn10_to_sbn (isbn_str)
	
	def _get_isbn13 (self):
		return self._isbn13
	
	def _set_isbn13 (self, isbn_str):
		isbn_str = utils.clean_isbn (isbn_str)
		assert (len (isbn_str) == 13)
		self._isbn13 = isbn_str
		self._isbn10 = utils.isbn13_to_isbn10 (isbn_str)
		if (self._isbn10):
			self._sbn = utils.isbn10_to_sbn (self._isbn10)
		else:
			self._sbn = None

	def _get_sbn (self):
		return self._sbn

	def _set_sbn (self, sbn_str):
		sbn_str = utils.clean_isbn (sbn_str)
		assert (len (sbn_str) == 9)
		self._sbn = sbn_str
		self._isbn10 = utils.sbn_to_isbn10 (sbn_str)
		self._isbn13 = utils.isbn10_to_isbn13 (self._isbn10)
	
	isbn10 = property (_get_isbn10, _set_isbn10)
	isbn13 = property (_get_isbn13, _set_isbn13)
	sbn = property (_get_sbn, _set_sbn)
	asin = isbn10
	ean = isbn10
	
	
### UTILITY FXNS


def clean_isbn (isbn_str):
	"""
	Strip whitepsace and punctuation from an ISBN representation.
	
	:Parameters:
		isbn_str : string
			The ISBN as a string, e.g. " 978-0-940016-73-6 "
			
	:Returns:
		A normalised ISBN, e.g. "9780940016736"
		
	For example::
	
		>>> clean_isbn ("3-8055-7505-X")
		'380557505X'
		>>> clean_isbn (" 0-940016-73-7  ")
		'0940016737'
		>>> clean_isbn ("978-0-940016-73-6")
		'9780940016736'
	
	"""
	# TODO: use regex to better clean whitespace?
	return isbn_str.replace (' ', '').replace ('-', '').upper()


def isbn10_to_isbn13 (isbn_str, cleanse=True):
	"""
	Convert an ISBN-10 to an ISBN-13.

	:Parameters:
		isbn_str : string
			The ISBN as a string, e.g. " 0-940016-73-6 ". It should be 10
			digits after normalisation.
		cleanse : boolean
			If true, formatting will be stripped from the ISBN before
			conversion.
			
	:Returns:
		A normalised ISBN-13, e.g. "9780940016736".

	
	For example::
	
		>>> isbn10_to_isbn13 ("0-940016-73-7")
		'9780940016736'
		>>> isbn10_to_isbn13 ("3-8055-7505-X")
		'9783805575058'
		>>> isbn10_to_isbn13 ("0940016737", cleanse=False)
		'9780940016736'
		>>> isbn10_to_isbn13 ("0-940016-73-7", cleanse=False)
		Traceback (most recent call last):
			...
		AssertionError: input '0-940016-73-7' is not 10 digits
		
	"""
	## Preconditions & preparation:
	if (cleanse):
		isbn_str = clean_isbn (isbn_str)
	assert (len (isbn_str) == 10), "input '%s' is not 10 digits" % isbn_str
	## Main:
	# drop the trailing check digit, add the new prefix
	isbn_str = '978' + isbn_str [:-1]
	# calc checksum
	isbn_str += isbn13_checksum (isbn_str)
	## Return:
	assert (len (isbn_str) == 13)
	return isbn_str
	
	
def isbn13_to_isbn10 (isbn_str, cleanse=True):
	"""
	Convert an ISBN-13 to an ISBN-10.
	
	:Parameters:
		isbn_str : string
			The ISBN as a string, e.g. " 0-940016-73-6 ". It should be 13
			digits after normalisation.
		cleanse : boolean
			If true, formatting will be stripped from the ISBN before
			conversion.

	:Returns:
		A normalaised ISBN-10, e.g. "0940016736", or ``None`` if no conversion
		is possible.
	
	For example::
	
		>>> isbn13_to_isbn10 ("978-0-940016-73-6")
		'0940016737'
		>>> isbn13_to_isbn10 ("9780940016736", cleanse=False)
		'0940016737'
		>>> isbn13_to_isbn10 ("979-1-234-56789-6")
		
		>>> isbn13_to_isbn10 ("978-3-8055-7505-8")
		'380557505X'
		>>> isbn13_to_isbn10 ("978-0-940016-73-6", cleanse=False)
		Traceback (most recent call last):
			...
		AssertionError: input '978-0-940016-73-6' is not 13 digits
		
	"""
	## Preconditions:
	if (cleanse):
		isbn_str = clean_isbn (isbn_str)
	assert (len (isbn_str) == 13), "input '%s' is not 13 digits" % isbn_str
	if (not isbn_str.startswith ('978')):
		return None
	## Main:
	isbn_str = isbn_str[3:-1]
	isbn_str += isbn10_checksum (isbn_str)
	## Return:
	assert (len (isbn_str) == 10), "output ISBN-10 is '%s'" % isbn_str
	return isbn_str


def isbn10_to_sbn (isbn_str, cleanse=True):
	"""
	Convert an ISBN-10 to an old-style SBN.
	
	:Parameters:
		isbn_str : string
			An ISBN-10 as a string, e.g. " 0-940016-73-6 ". It should be 10
			digits after normalisation.
		cleanse : boolean
			If true, formatting will be stripped from the ISBN before
			conversion.

	:Returns:
		A normalised SBN, e.g. "940016736", or ``None`` if no conversion
		is possible.
	
	For example::
	
		>>> isbn10_to_sbn ("0-940016-73-7")
		'940016737'
		>>> isbn10_to_sbn ("0940016737", cleanse=False)
		'940016737'
		>>> isbn10_to_sbn ("1-56414-682-0")
		
		>>> isbn10_to_sbn ("0-940016-73-7", cleanse=False)
		Traceback (most recent call last):
			...
		AssertionError: input '0-940016-73-7' is not 10 digits
		
	This is done simply by cropping a leading 0. Invalid ISBNs are simply
	returned as ``None``.

	"""
	## Preconditions:
	if (cleanse):
		isbn_str = clean_isbn (isbn_str)
	assert (len (isbn_str) == 10), "input '%s' is not 10 digits" % isbn_str
	## Main:
	if (isbn_str.startswith ('0')):
		return isbn_str[1:]
	else:
		return None


def sbn_to_isbn10 (sbn_str, cleanse=True):
	"""
	Convert an old-style SBN to an ISBN-10.

	:Parameters:
		sbn_str : string
			An SBN as a string, e.g. " 940016-73-6 ". It should be 9
			digits after normalisation.
		cleanse : boolean
			If true, formatting will be stripped from the ISBN before
			conversion.

	:Returns:
		A normalised ISBN-10, e.g. "0940016736".
	
	:Exceptions:
		AssertionError
			If the input isn't a 9-digit SBN.
	
	The conversion from an SBN to ISBN-10 is trivial (add a '0' prefix), but
	is provided for orthogonality.
	
	For example::

		>>> sbn_to_isbn10 ("940016-73-7")
		'0940016737'
		>>> sbn_to_isbn10 ("940016737", cleanse=False)
		'0940016737'
		
	"""
	## Preconditions:
	if (cleanse):
		sbn_str = clean_isbn (sbn_str)
	assert (len (sbn_str) == 9), "input '%s' is not 9 digits" % sbn_str
	## Main:
	return '0' + sbn_str



def isbn13_checksum (isbn_str):
	"""
	Return the checksum over the coding (first 12 digits) of an ISBN-13.

	:Parameters:
		isbn_str : string
			An ISBN-13 without the trailing checksum digit.

	:Returns:
		The checksum character, ``0`` to ``9``.

	For example:

		>>> isbn13_checksum ("978094001673")
		'6'
		>>> isbn13_checksum ("979123456789")
		'6'

	"""
	## Preconditions & preparation:
	assert (len (isbn_str) == 12), 'expecting a 12-digit string'
	## Main:
	csum = 0
	for i in range (0, len (isbn_str), 2):
		csum += int (isbn_str[i]) + (3 * int (isbn_str[i+1]))
	cdigit = 10 - (csum % 10)
	if (cdigit == 10):
		cdigit = 0
	## Return:
	return str (cdigit)
		
		
def isbn10_checksum (isbn_str):
	"""
	Return the checksum over the coding (first 9 digits) of an ISBN-10.
	
	:Parameters:
		isbn_str : string
			An ISBN-10 without the trailing checksum digit.
			
	:Returns:
		The checksum character, ``0`` to ``9`` and ``X``.
		
	For example:
	
		>>> isbn10_checksum ("094001673")
		'7'
		>>> isbn10_checksum ("380557505")
		'X'
	
	This is identical to the SBN checksum.
	
	"""
	## Preconditions & preparation:
	assert (len (isbn_str) == 9), 'expecting a 9-digit string'
	## Main:
	csum = 0
	for i in range (len (isbn_str)):
		csum += (i+1) * int (isbn_str[i])
	cdigit = csum % 11
	if (cdigit == 10):
		cdigit = 'X'
	## Return:
	return str (cdigit)


def sbn_checksum (sbn_str):
	"""
	Return the checksum over the coding (first 8 digits) of an SBN.
	
	:Parameters:
		sbn_str : string
			An SBN without the trailing checksum digit.
			
	:Returns:
		The checksum character, ``0`` to ``9`` or ``X``.
		
	For example:
	
		>>> sbn_checksum ("94001673")
		'7'
	
	
	"""
	## Preconditions & preparation:
	assert (len (sbn_str) == 8), 'expecting a 8-digit string'
	## Return:
	return isbn10_checksum ('0' + sbn_str)


def validate_isbn (isbn_str):
	"""
	Check if a book number is valid, via the trailing checksum digit.
	
	:Parameters:
		isbn_str : string
			An ISBN
			
	:Returns:
		True or false, for whether the number if valid or not.
	
	For example::
		
		>>> validate_isbn ("940016737")
		True
		>>> validate_isbn ("3-8055-7505-X")
		True
		>>> validate_isbn ("3-8055-7505-3")
		False
		
		
	"""
	## Preconditions & preparation:
	isbn_str = clean_isbn (isbn_str)
	## Main:
	coding, csum = isbn_str[:-1], isbn_str[-1]
	if (len (isbn_str) == 13):
		csum_func = isbn13_checksum
	elif (len (isbn_str) == 10):
		csum_func = isbn10_checksum
	elif (len (isbn_str) == 9):
		csum_func = sbn_checksum
	else:
		raise ValueError ("ISBN '%s' of unrecognised length" % isbn_str)
	new_csum = csum_func (isbn_str[:-1])
	## Return:
	return (new_csum == csum)


	