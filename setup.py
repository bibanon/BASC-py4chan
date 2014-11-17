#!/usr/bin/env python

"""
    py-4chan-setup
    ~~~~~~~~~~~~~~

    Python Wrappers to access 4chan's API.

    This program is free software. It comes without any warranty, to
    the extent permitted by applicable law. You can redistribute it
    and/or modify it under the terms of the Do What The Fuck You Want
    To Public License, Version 2, as published by Sam Hocevar. See
    http://sam.zoy.org/wtfpl/COPYING for more details.

"""

from setuptools import setup
from py4chan import __version__

setup(name='BASC-py4chan',
    version=__version__,
    description='Python 4chan API Wrapper. Improved version of Edgeworth\'s original py-4chan wrapper.',
    long_description = open('README.rst').read(), 
    license=open('LICENSE').read(),
    author='Antonizoon (Lawrence Wu)',
    author_email='sagnessagiel@gmail.com',
    url='http://github.com/bibanon/BASC-py4chan',
    packages=['py4chan'],
    package_data={'': ['README.md', 'LICENSE']},
    install_requires=['requests >= 1.0.0']
)