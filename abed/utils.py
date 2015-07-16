"""
Various utility functions used throughout abed

"""

import errno
import os

from abed import settings

basename = os.path.basename
splitext = os.path.splitext

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

def hash_from_filename(filename):
    bname = basename(filename)
    exts = splitext(bname)
    start = exts[0]
    hsh = int(start)
    return hsh

def dataset_name(dset):
    if hasattr(settings, 'DATASET_NAMES'):
        return str(settings.DATASET_NAMES[dset])
    if isinstance(dset, tuple):
        txt = ''
        for name in dset:
            bname = basename(name)
            exts = splitext(bname)
            start = exts[0]
            txt += start + '_'
        txt = txt.rstrip('_')
    else:
        bname = basename(dset)
        exts = splitext(bname)
        start = exts[0]
        txt = start
    return txt

