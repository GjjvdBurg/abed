"""
Functions for dealing with zips of results

"""

import os
import shutil
import tarfile

from abed import settings
from abed.run_utils import get_output_dir

def unpack_zips():
    bzips = (x for x in os.listdir(settings.ZIP_DIR) if x.endswith('.bz2'))
    for fname in bzips:
        tar = tarfile.open(fname, 'r:bz2')
        tar.extractall(settings.STAGE_DIR)
        tar.close()
        move_results()
        clean_empty_dir(settings.STAGE_DIR)

def move_results():
    subdirs = os.listdir(settings.STAGE_DIR)
    for subdir in subdirs:
        files = os.listdir(subdir)
        for fname in files:
            fpath = '%s/%s/%s' % (settings.STAGE_DIR, subdir, fname)
            newsubdir = get_output_dir(settings.RESULT_DIR)
            dpath = '%s/%s/%s' % (settings.RESULT_DIR, newsubdir, fname)
            shutil.move(fpath, dpath)

def clean_empty_dir(folder):
    try:
        os.rmdir(folder)
    except OSError:
        dirs = (x for x in os.listdir(folder) if os.path.isdir(x))
        for d in dirs:
            clean_empty_dir(d)
