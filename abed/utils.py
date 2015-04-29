"""
Various utility functions used throughout ABED

"""

import errno
import os

from termcolor import cprint

def info(txt):
    cprint(txt, 'yellow')

def error(txt):
    cprint(txt, 'red')

def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
