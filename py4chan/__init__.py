"""
    basc_py-4chan
    ~~~~~~~~

    Python Wrappers to access 4chan's API.

    This program is free software. It comes without any warranty, to
    the extent permitted by applicable law. You can redistribute it
    and/or modify it under the terms of the Do What The Fuck You Want
    To Public License, Version 2, as published by Sam Hocevar. See
    http://sam.zoy.org/wtfpl/COPYING for more details.

"""

__version__ = '0.4.2'

from .board import Board, board, get_boards
from .thread import Thread
from .post import Post
