"""
Functions for compressing result directories.

"""

import tarfile
import os
from subprocess import check_output, CalledProcessError, STDOUT

from abed.conf import settings
from abed.datasets import dataset_name
from abed.utils import error, info, hash_from_filename
from abed.progress import iter_progress
from abed.results.walk import files_w_dataset

def dataset_completed(dsetfiles, dset, task_dict):
    if settings.TYPE == 'ASSESS':
        dset_tasks = {k:v for k, v in task_dict.iteritems() if
                v['dataset'] == dset}
    elif settings.TYPE == 'CV_TT':
        dset_tasks = {k:v for k, v in task_dict.iteritems() if
                (v['train_dataset'] == dset[0] and
                    v['test_dataset'] == dset[1])}
    else:
        error("Compressing data not supported for TYPE = %s" % settings.TYPE)
        raise SystemExit
    have_hashes = set([hash_from_filename(f) for f in dsetfiles])
    need_hashes = set(dset_tasks.keys())
    return have_hashes == need_hashes

def compress_dataset(dset):
    dsetname = dataset_name(dset)
    dsetpath = os.path.join(settings.RESULT_DIR, dsetname)
    dsetpath = dsetpath.rstrip(os.sep)
    if settings.COMPRESSION == 'bzip2':
        extension = 'bz2'
    elif settings.COMPRESSION == 'gzip':
        extension = 'gz'
    elif settings.COMPRESSION == 'lzma':
        extension = 'xz'
    else:
        error("Unknown compression algorithm specified in "
                "COMPRESSION configuration. Please check the "
                "configuration file.")
        raise SystemExit
    output_filename = '%s.tar.%s' % (dsetpath, extension)
    # lzma will be available in tarfile when abed is ported to Python 3. On
    # posix systems we can try compressing with the tar command.
    if os.name == 'posix' and settings.COMPRESSION == 'lzma':
        try:
            cmd = ('XZ_OPT=-9 tar --directory=%s -Jcf %s %s' %
                    (settings.RESULT_DIR, output_filename, dsetname))
            check_output(cmd, stderr=STDOUT, shell=True)
        except CalledProcessError:
            error("There was an error executing '%s'.")
            raise SystemExit
    elif settings.COMPRESSION == 'lzma':
        error("lzma compression is not yet available for your platform.")
        raise SystemExit
    else:
        mode = 'w:%s' % extension
        with tarfile.open(output_filename, mode, compresslevel=9) as tar:
            tar.add(dsetpath, arcname=os.path.basename(dsetpath))

def compress_results(task_dict):
    completed_dsets = []
    for dset in settings.DATASETS:
        try:
            files = [f for f in files_w_dataset(dset)]
        except:
            continue
        if dataset_completed(files, dset, task_dict):
            completed_dsets.append(dset)

    info("Starting compression of %i completed result directories." %
            len(completed_dsets))
    for dset in iter_progress(completed_dsets, 'Datasets'):
        compress_dataset(dset)
