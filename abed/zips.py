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
from abed.progress import iter_progress
from abed.tasks import init_tasks
from abed.utils import error, mkdir

splitext = os.path.splitext
basename = os.path.basename

def _unpack_zip(zipfile, all_tasks):
    fpath = '%s%s%s' % (settings.ZIP_DIR, os.sep, zipfile)
    try:
        b = bz2file.BZ2File(fpath)
        tar = tarfile.open(fileobj=b)
    except tarfile.ReadError:
        error("Could not read tarfile: %s" % fpath)
        return
    tar.extractall(settings.STAGE_DIR)
    tar.close()
    move_results(all_tasks)
    ziplog = settings.ZIP_DIR + os.sep + 'abed_unzipped.txt'
    with open(ziplog, 'a') as fid:
        fid.write(zipfile + '\n')

def unpack_zips():
    ziplog = settings.ZIP_DIR + os.sep + 'abed_unzipped.txt'
    if os.path.exists(ziplog):
        with open(ziplog, 'r') as fid:
            unzipped = [x.strip() for x in fid.readlines()]
    else:
        unzipped = []
    all_tasks = init_tasks()
    bzips = [x for x in os.listdir(settings.ZIP_DIR) if x.endswith('.bz2') and 
            not x in unzipped]
    for fname in iter_progress(bzips, 'Unpacking zips: '):
        _unpack_zip(fname, all_tasks)

def move_results(task_dict):
    mkdir(settings.RESULT_DIR)
    subdirs = os.listdir(settings.STAGE_DIR)
    for subdir in subdirs:
        subpath = '%s%s%s' % (settings.STAGE_DIR, os.sep, subdir)
        files = os.listdir(subpath)
        for fname in files:
            fpath = '%s%s%s' % (subpath, os.sep, fname)
            hsh = int(splitext(basename(fpath))[0])
            dset = splitext(basename(task_dict[hsh]['dataset']))[0]
            method = task_dict[hsh]['method']
            outdir = '%s%s%s%s%s' % (settings.RESULT_DIR, os.sep, dset, os.sep, 
                    method)
            mkdir(outdir)
            dpath = '%s%s%s' % (outdir, os.sep, fname)
            shutil.move(fpath, dpath)
        clean_empty_dir(subpath)

def clean_empty_dir(folder):
    try:
        os.rmdir(folder)
    except OSError:
        dirs = (x for x in os.listdir(folder) if os.path.isdir(x))
        for d in dirs:
            clean_empty_dir(d)
