#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A setup script using setuptools.

If run like this::

	python setup.py install

it will install itself into the appropriate python's site packages. Although
not everyone will have setuptools, ``ez_setup.py`` is included as a bootstrap.
Those who do have setuptools, but don't have a constant internet connection
can always download a package or egg. Those who have neither are kinda stuck.

"""

### IMPORTS ###

# ensure setuptools is available
#from ez_setup import use_setuptools
#use_setuptools()
from setuptools import setup, find_packages
import sys, os


### CONSTANTS & DEFINES ###

from biblio.isbn import __version__


### SETUP ###

setup(
	name='biblio.isbn',
	version=__version__,
	description="Handling and converting ISBN numbers",
	long_description=open("README.txt").read() + "\n" +
		open (os.path.join ("doc", "HISTORY.txt")).read(),
	classifiers=[
		"Programming Language :: Python",
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: BSD License',
		"Topic :: Software Development :: Libraries :: Python Modules",
	],
	keywords='ISBN SBN ASIN',
	author='Paul-Michael Agapow',
	author_email='agapow@bbsrc.ac.uk',
	url='http://www.agapow.net/software/biblioisbn',
	license='BSD',
	packages=find_packages(exclude=['ez_setup', 'tests', 'test']),
	test_suite = 'nose.collector',
	namespace_packages=['biblio'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		'setuptools',
		# -*- Extra requirements: -*-
	],
	entry_points="""
		# -*- Entry points: -*-
	""",
)


### END ###

