# -*- coding: utf-8 -*-

"""
I/O stuff
"""

import sys


def info(txt):
    message = "%s" % txt
    print(message, file=sys.stdout)
    sys.stdout.flush()


def error(txt):
    message = "Error: %s" % (txt)
    print(message, file=sys.stderr)
    sys.stderr.flush()


def warning(txt):
    message = "Warning: %s" % (txt)
    print(message, file=sys.stderr)
    sys.stderr.flush()
