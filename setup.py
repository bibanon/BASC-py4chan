#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""4chan Python Library.

BASC-py4chan is a Python library that gives access to the 4chan API
and an object-oriented way to browse and get board and thread
information quickly and easily.

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
the LICENSE file for more details.
"""

from setuptools import setup
from basc_py4chan import __version__

setup(
    name='BASC-py4chan',
    version=__version__,
    description=("Python 4chan API Wrapper. Improved version of Edgeworth's "
                 "original py-4chan wrapper."),
    long_description=open('README.rst').read(),
    license=open('LICENSE').read(),
    author='Antonizoon (Antonizoon Overtwater)',
    author_email='antonizoon@bibanon.org',
    url='http://github.com/bibanon/BASC-py4chan',
    packages=['basc_py4chan'],
    package_dir={
        'basc_py4chan': 'basc_py4chan',
    },
    package_data={'': ['README.rst', 'LICENSE']},
    install_requires=['requests >= 1.0.0'],
    keywords='4chan api',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
