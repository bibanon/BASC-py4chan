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
from py4chan import _VERSION

setup(name='BASC-py4chan',
    version=_VERSION,
    description='Improved version of Edgeworth\'s Python 4chan API Wrapper.',
    author='Lawrence Wu (antonizoon)',
    author_email='sagnessagiel@gmail.com',
    url='http://github.com/bibanon/BASC-py4chan',
    license="http://sam.zoy.org/wtfpl/COPYING",
    packages=['py4chan'],
    install_requires = ['requests >= 1.0.0']
)