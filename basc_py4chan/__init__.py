#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# the LICENSE file for more details.
"""4chan Python Library.

BASC-py4chan is a Python library that gives access to the 4chan API
and an object-oriented way to browse and get board and thread
information quickly and easily.
"""

__version__ = '0.5.5'

from .board import Board, board, get_boards, get_all_boards
from .thread import Thread
from .post import Post
