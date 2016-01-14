"""
Various utility functions used throughout abed

"""

from __future__ import print_function

import datetime
import errno
import os
import sys

basename = os.path.basename
splitext = os.path.splitext

def colorprint(s, color=None, sep='', end='\n', file=sys.stdout):
    """
        Function for printing output to stdout in colour. Simply an extension of 
        the Python 3 print function which supports colour by adding a shell 
        colour code. Available colors are: purple, blue, gree, yellow, and red.

    """
    purple = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    endc = '\033[0m'
    if color is None:
        print(s, sep=sep, end=end, file=file)
    else:
        color = color.lower()
        if color == 'blue':
            print(blue + s + endc, sep=sep, end=end, file=file)
        elif color == 'red':
            print(red + s + endc, sep=sep, end=end, file=file)
        elif color == 'green':
            print(green + s+ endc, sep=sep, end=end, file=file)
        elif color == 'yellow':
            print(yellow + s + endc, sep=sep, end=end, file=file)
        elif color == 'purple':
            print(purple + s + endc, sep=sep, end=end, file=file)
        else:
            print(s, sep=sep, end=end, file=file)

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

def info(txt, color_wrap=True):
    dt = datetime.datetime.now()
    message = '[ABED INFO || %s]: %s' % (dt.strftime('%c'), txt)
    if color_wrap:
        wrapped = wrap_text(message)
        colorprint(wrapped, 'green')
    else:
        print(message)

def error(txt, color_wrap=True):
    dt = datetime.datetime.now()
    message = '[ABED ERROR || %s]: %s' % (dt.strftime('%c'), txt)
    if color_wrap:
        wrapped = wrap_text(message)
        colorprint(wrapped, 'red')
    else:
        print(message)

def warning(txt, color_wrap=True):
    dt = datetime.datetime.now()
    message = '[ABED WARNING || %s]: %s' % (dt.strftime('%c'), txt)
    if color_wrap:
        wrapped = wrap_text(message)
        colorprint(wrapped, 'yellow')
    else:
        print(message)

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
