#!/usr/bin/env python

from distutils.core import setup
from py4chan import _VERSION

setup(name='py-4chan',
    version=_VERSION,
    description='Python 4chan API Wrapper',
    author='Edgeworth Euler',
    author_email='e@encyclopediadramatica.se',
    url='http://github.com/e000/py-4chan',
    packages=['py4chan']
)