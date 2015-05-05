"""
Functions for dealing with zips of results

Note:
    The bz2file dependency is needed because tar.bz2 files are created with 
    pbzip2, which results in multiple streams in the tarfile. The Python 2.x 
    tarfile module does not handle multiple streams, but the bz2file package 
    does. Unpacking the tarfiles is thus done in two separate steps.

"""

import bz2file
import os
import shutil
import tarfile

from abed import settings
from abed.run_utils import get_output_dir
from abed.utils import error, info, mkdir

def unpack_zips():
    bzips = (x for x in os.listdir(settings.ZIP_DIR) if x.endswith('.bz2'))
    for fname in bzips:
        info("Unpacking zip file: %s" % fname)
        fpath = '%s%s%s' % (settings.ZIP_DIR, os.sep, fname)
        try:
            b = bz2file.BZ2File(fpath)
            tar = tarfile.open(fileobj=b)
        except tarfile.ReadError:
            error("Could not read tarfile: %s" % fpath)
            continue
        tar.extractall(settings.STAGE_DIR)
        tar.close()
        move_results()
        clean_empty_dir(settings.STAGE_DIR)

def move_results():
    mkdir(settings.RESULT_DIR)
    subdirs = os.listdir(settings.STAGE_DIR)
    for subdir in subdirs:
        subpath = '%s%s%s' % (settings.STAGE_DIR, os.sep, subdir)
        files = os.listdir(subpath)
        for fname in files:
            fpath = '%s%s%s' % (subpath, os.sep, fname)
            newsubdir = get_output_dir(settings.RESULT_DIR)
            dpath = '%s%s%s' % (newsubdir, os.sep, fname)
            info("Moving %s" % (fname))
            shutil.move(fpath, dpath)

def clean_empty_dir(folder):
    try:
        os.rmdir(folder)
    except OSError:
        dirs = (x for x in os.listdir(folder) if os.path.isdir(x))
        for d in dirs:
            clean_empty_dir(d)
