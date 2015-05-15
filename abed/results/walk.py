"""
Generators for iterating over all result files

"""

import os

from abed import settings
from abed.exceptions import (AbedDatasetdirNotFoundException, 
        AbedMethoddirNotFoundException)

basename = os.path.basename
splitext = os.path.splitext

def files_w_method(method):
    for dset in os.listdir(settings.RESULT_DIR):
        dpath = '%s%s%s' % (settings.RESULT_DIR, os.sep, dset)
        methdirs = os.listdir(dpath)
        if not method in methdirs:
            raise AbedMethoddirNotFoundException
        mpath = '%s%s%s' % (dpath, os.sep, method)
        for f in os.listdir(mpath):
            fname = '%s%s%s' % (mpath, os.sep, f)
            yield fname

def files_w_dataset(dataset):
    dset = splitext(basename(dataset))[0]
    if dset not in os.listdir(settings.RESULT_DIR):
        raise AbedDatasetdirNotFoundException
    dpath = '%s%s%s' % (settings.RESULT_DIR, os.sep, dset)
    for method in os.listdir(dpath):
        mpath = '%s%s%s' % (dpath, os.sep, method)
        for f in os.listdir(mpath):
            fname = '%s%s%s' % (mpath, os.sep, f)
            yield fname

def files_w_dset_and_method(dataset, method):
    dset = splitext(basename(dataset))[0]
    if dset not in os.listdir(settings.RESULT_DIR):
        raise AbedDatasetdirNotFoundException(dset)
    dpath = '%s%s%s' % (settings.RESULT_DIR, os.sep, dset)
    methdirs = os.listdir(dpath)
    if not method in methdirs:
         raise AbedMethoddirNotFoundException(method)
    mpath = '%s%s%s' % (dpath, os.sep, method)
    for f in os.listdir(mpath):
        fname = '%s%s%s' % (mpath, os.sep, f)
        yield fname

def walk_results():
    for dataset in settings.DATASETS:
        dset = splitext(basename(dataset))[0]
        if dset not in os.listdir(settings.RESULT_DIR):
            continue
        dpath = '%s%s%s' % (settings.RESULT_DIR, os.sep, dset)
        for method in settings.METHODS:
            if method not in os.listdir(dpath):
                continue
            mpath = '%s%s%s' % (dpath, os.sep, method)
            files = ['%s%s%s' % (mpath, os.sep, f) for f in os.listdir(mpath)]
            yield dset, method, files
