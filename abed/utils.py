"""
Various utility functions used throughout abed

"""

import errno
import os

def info(txt):
    print('[ABED INFO]: ' + txt)

def error(txt):
    print('[ABED ERROR]: ' + txt)

def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
