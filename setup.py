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

from distutils.core import setup
#from py4chan import _VERSION		# Causes issues with requests-transition, when requests is not already installed. Use workaround
_VERSION = '0.1.3'

# Use requirements.txt file for dependencies
# Disabled, because it doesn't work with PyPi
#REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
REQUIREMENTS = 'requests-transition'

setup(name='py-4chan',
    version=_VERSION,
    description='Python 4chan API Wrapper',
    author='Edgeworth Euler',
    author_email='e@encyclopediadramatica.se',
    url='http://github.com/e000/py-4chan',
    license="http://sam.zoy.org/wtfpl/COPYING",
    packages=['py4chan'],
    install_requires = REQUIREMENTS,
)