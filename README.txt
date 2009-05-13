Introduction
------------

Although International Standard Book Numbers have been issued as ISBN-13s for
some years, users still have to cope with a large number of legacy ISBN-10s.
This package provides functions for converting between ISBN types and
stripping ISBNs, encapsulating these in a simple class.


Usage
-----

`biblio.isbn` provides functions for converting and checking ISBNs and a class, that encapsulates those. For example::

	>>> from biblio.isbn import isbn10_to_isbn13, isbn13_to_isbn10
	>>> isbn10_to_isbn13 ("0-940016-73-7")
	'9780940016736'
	>>> isbn13_to_isbn10 ("978-3-8055-7505-8")
	'380557505X'
	>>> from biblio.isbn import Isbn
	>>> my_isbn = Isbn ("0-940016-73-7")
	>>> my_isbn.isbn10
	'0940016737'
	>>> my_isbn.isbn13
	'9780940016736'
	>>> my_isbn.asin
	'0940016737'
	>>> my_isbn.sbn
	'940016737'


Caveats and bugs
----------------

Formatting and whitespace is stripped before an ISBN is parsed. It would be
useful to include functionality for the reverse, consistently formatting
ISBNs. However the length of the internal fields can vary (while still adding
up to the same length), and without extensive lists of group and publisher
codes, it is impossible.

Given that all SBNs have an equivalent ISBN-10 (but not vice-versa) and all
ISBN-10s have an equivalent ISBN-13 (but not vice-versa), the question of how
to handle failed conversions arises. Rather than have the user guess which
codes are convertible, or be forced to try conversion and catch exceptions,
failed conversions return ``None``.


References
----------

* James Rowe has released `an ISBN module
  <http://pypi.python.org/pypi/pyisbn/>`__ already. (If I'd known of its
  existence, I probably wouldn't have written this package.)

* `Wikipedia on ISBNs
  <http://en.wikipedia.org/wiki/International_Standard_Book_Number>`__

* The Book Industry Study group on `ISBN-13 for Dummies
  <http://www.bisg.org/isbn-13/for.dummies.html>`__ and `Converting ISBNs
  <http://www.bisg.org/isbn-13/conversions.html>`__

* `isbntools.com <http://isbntools.com/>`__ which includes a Java ISBN class.

"""