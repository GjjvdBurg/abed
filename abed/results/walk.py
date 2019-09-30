"""
Generators for iterating over all result files

"""

import os
import tarfile

from backports import lzma

from ..conf import settings
from ..datasets import dataset_name
from ..exceptions import (
    AbedDatasetdirNotFoundException,
    AbedMethoddirNotFoundException,
)
from ..progress import iter_progress
from ..utils import hash_from_filename

basename = os.path.basename
splitext = os.path.splitext


def files_w_method(method):
    for dset in os.listdir(settings.RESULT_DIR):
        dpath = "%s%s%s" % (settings.RESULT_DIR, os.sep, dset)
        methdirs = os.listdir(dpath)
        if not method in methdirs:
            raise AbedMethoddirNotFoundException
        mpath = "%s%s%s" % (dpath, os.sep, method)
        for f in os.listdir(mpath):
            fname = "%s%s%s" % (mpath, os.sep, f)
            yield fname


def files_w_dataset(dataset):
    dset = dataset_name(dataset)
    if dset not in os.listdir(settings.RESULT_DIR):
        raise AbedDatasetdirNotFoundException
    dpath = "%s%s%s" % (settings.RESULT_DIR, os.sep, dset)
    for method in os.listdir(dpath):
        mpath = "%s%s%s" % (dpath, os.sep, method)
        for f in os.listdir(mpath):
            fname = "%s%s%s" % (mpath, os.sep, f)
            yield fname


def files_w_dset_and_method(dataset, method):
    dset = dataset_name(dataset)
    if dset not in os.listdir(settings.RESULT_DIR):
        raise AbedDatasetdirNotFoundException(dset)
    dpath = "%s%s%s" % (settings.RESULT_DIR, os.sep, dset)
    methdirs = os.listdir(dpath)
    if not method in methdirs:
        raise AbedMethoddirNotFoundException(method)
    mpath = "%s%s%s" % (dpath, os.sep, method)
    for f in os.listdir(mpath):
        fname = "%s%s%s" % (mpath, os.sep, f)
        yield fname


def walk_hashes():
    results = os.listdir(settings.RESULT_DIR)
    for dataset in iter_progress(settings.DATASETS):
        dset = dataset_name(dataset)
        if dset in results:
            for hsh in walk_dir_hashes(dataset, dset):
                yield hsh
        tarstr = "%s.tar" % dset
        if any([x.startswith(tarstr) for x in results]):
            fname = next((x for x in results if x.startswith(tarstr)), None)
            for hsh in walk_archive_hashes(dataset, dset, fname):
                yield hsh


def walk_dir_hashes(dataset, dset):
    dpath = "%s%s%s" % (settings.RESULT_DIR, os.sep, dset)
    for method in settings.METHODS:
        if method not in os.listdir(dpath):
            continue
        mpath = "%s%s%s" % (dpath, os.sep, method)
        files = ["%s%s%s" % (mpath, os.sep, f) for f in os.listdir(mpath)]
        for f in files:
            hsh = hash_from_filename(f)
            yield hsh


def walk_archive_hashes(dataset, dset, fname):
    fpath = os.path.join(settings.RESULT_DIR, fname)
    if fname.endswith("bz2"):
        tar = tarfile.open(fpath, "r:bz2")
    elif fname.endswith("gz"):
        tar = tarfile.open(fpath, "r:gz")
    else:
        l = lzma.open(fpath, "r")
        tar = tarfile.open(fileobj=l)
    for tarinfo in tar:
        if not tarinfo.isreg():
            continue
        hsh = hash_from_filename(tarinfo.name)
        yield hsh


def walk_for_cache(ac):
    results = os.listdir(settings.RESULT_DIR)
    for dataset in iter_progress(settings.DATASETS):
        dset = dataset_name(dataset)
        if dset in results:
            for d, m, f, h in walk_directory(dataset, dset, ac):
                yield d, m, f, h
        tarstr = "%s.tar" % dset
        if any([x.startswith(tarstr) for x in results]):
            fname = next((x for x in results if x.startswith(tarstr)), None)
            for d, m, f, h in walk_archive(dataset, dset, fname, ac):
                yield d, m, f, h


def walk_directory(dataset, dset, ac):
    dpath = "%s%s%s" % (settings.RESULT_DIR, os.sep, dset)
    for method in settings.METHODS:
        if not method in os.listdir(dpath):
            continue
        mpath = "%s%s%s" % (dpath, os.sep, method)
        files = ["%s%s%s" % (mpath, os.sep, f) for f in os.listdir(mpath)]
        for fpath in files:
            hsh = hash_from_filename(fpath)
            if not ac.has_result(hsh):
                fid = open(fpath, "r")
                yield dataset, method, fid, hsh


def walk_tar(tar, ac):
    for tarinfo in tar:
        if not tarinfo.isreg():
            continue
        hsh = hash_from_filename(tarinfo.name)
        if not ac.has_result(hsh):
            fid = tar.extractfile(tarinfo)
            tar_dset = tarinfo.name.split("/")[0]
            dataset = next(
                (x for x in settings.DATASETS if dataset_name(x) == tar_dset),
                None,
            )
            tar_mth = tarinfo.name.split("/")[1]
            method = next((x for x in settings.METHODS if x == tar_mth), None)
            yield dataset, method, fid, hsh


def walk_archive(dataset, dset, fname, ac):
    fpath = os.path.join(settings.RESULT_DIR, fname)
    if fname.endswith("bz2"):
        tar = tarfile.open(fpath, "r:bz2")
    elif fname.endswith("gz"):
        tar = tarfile.open(fpath, "r:gz")
    else:
        l = lzma.open(fpath, "r")
        tar = tarfile.open(fileobj=l)
    return walk_tar(tar, ac)
