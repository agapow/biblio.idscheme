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
	
	
	