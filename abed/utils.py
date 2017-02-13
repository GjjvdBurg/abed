"""
Various utility functions used throughout abed

"""

from __future__ import print_function

import errno
import os
import sys

basename = os.path.basename
splitext = os.path.splitext


def wrap_text(text, max_length=120):
    """
    Wraps the words into lines of a fixed length for prettier printing.
    """

    words = []
    for part in text.split('\n'):
        words.extend(part.split(' '))
        words.append('\n')
    sentences = []
    current_length = 0
    sentence = ''
    for word in words:
        if word == '\n':
            sentences.append(sentence)
            sentence = ''
            current_length = 0
            continue
        if (current_length + len(word) + 1 <= max_length):
            current_length += len(word) + 1
            sentence += word + ' '
        else:
            current_length = len(word) + 1
            sentences.append(sentence)
            sentence = word + ' '
    return '\n'.join(sentences)


def info(txt):
    message = '%s' % txt
    print(message)


def error(txt):
    message = 'Error: %s' % (txt)
    print(message, file=sys.stderr)


def warning(txt):
    message = 'Warning: %s' % (txt)
    print(message, file=sys.stderr)


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def hash_from_filename(filename):
    bname = basename(filename)
    exts = splitext(bname)
    start = exts[0]
    hsh = int(start)
    return hsh

def clean_str(string):
    return '_'.join(string.split(' ')).lower()

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)
