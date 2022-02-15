"""Functions for compressing result directories.

The functions in this module are used to compress results files for datasets 
that are completely finished. This can be useful for when raw results need to 
be stored on disk, but storage space is sparse. The compression algorithm used 
can be set by the user in the configuration file (:setting:`COMPRESSION` 
setting).  All compressed files are tar files, generated with the highest 
possible compression setting.

"""

import six
import tarfile
import os

from subprocess import check_output, CalledProcessError, STDOUT

from .conf import settings
from .datasets import dataset_name
from .io import error, info
from .utils import hash_from_filename
from .progress import iter_progress
from .results.walk import files_w_dataset


def dataset_completed(dsetfiles, dset, task_dict):
    """Check if a given dataset is complete

    This function checks if all results for a given dataset are available on
    disk. This is done by checking if all hashes for the specified dataset are
    available.

    Parameters
    ----------
    dsetfiles : list
        Filenames of files relating to this dataset
    dset : str/tuple
        The name of the dataset. Depending on the type of experiments that were
        done this is either a string or a tuple of strings
    task_dict : dict
        The dict with the mappings from hashes to command dicts, as returned by
        :func:`.tasks.init_tasks`.

    Returns
    -------
    bool
        Whether or not all results for the given dataset are available.

    Raises
    ------
    SystemExit
        When trying to compress results for an experiment type which does not
        support result compression (for instance when using RAW mode), an error
        is printed and the program exits.


    """
    if settings.TYPE in ("ASSESS", "ASSESS_GRID", "ASSESS_LIST"):
        dset_tasks = {k: v for k, v in task_dict.items() if v["dataset"] == dset}
    elif settings.TYPE == "CV_TT":
        dset_tasks = {
            k: v
            for k, v in task_dict.items()
            if (v["train_dataset"] == dset[0] and v["test_dataset"] == dset[1])
        }
    else:
        error("Compressing data not supported for TYPE = %s" % settings.TYPE)
        raise SystemExit
    have_hashes = set([hash_from_filename(f) for f in dsetfiles])
    need_hashes = set(dset_tasks.keys())
    return have_hashes == need_hashes


def compress_dataset(dset):
    """Compress results of a given dataset

    This function compresses the results for a given dataset into a compressed
    tar file. This is done through the tarfile module for the gzip and bzip2
    compression algorithms. When lzma is used, the tarfile module can only be
    used when ABED is run through Python 3 (as lzma compression is not
    available in the Python 2 tarfile package). When running on Python 2 on a
    posix platform however, we assume that lzma compression is available in the
    ``tar`` command. Therefore, in this case the result directory is compressed
    using a call to ``tar``.

    In all cases, the highest compression level is used, to save as much disk
    space as possible.

    Parameters
    ----------
    dset : str/tuple
        The name of the dataset. Depending on the type of experiments that were
        done this is either a string or a tuple of strings

    Notes
    -----
    ABED doesn't remove the existing folder, so this should be done by the
    user.

    Raises
    ------
    SystemExit
        When an unknown compression algorithm is specified, when lzma
        compression is requested on an unsupported platform, or when an error
        occurs with the external ``tar`` command, the program exits.

    """
    dsetname = dataset_name(dset)
    dsetpath = os.path.join(settings.RESULT_DIR, dsetname)
    dsetpath = dsetpath.rstrip(os.sep)

    if settings.COMPRESSION == "bzip2":
        extension = "bz2"
    elif settings.COMPRESSION == "gzip":
        extension = "gz"
    elif settings.COMPRESSION == "lzma":
        extension = "xz"
    else:
        error(
            "Unknown compression algorithm specified in "
            "COMPRESSION configuration. Please check the "
            "configuration file."
        )
        raise SystemExit
    output_filename = "%s.tar.%s" % (dsetpath, extension)

    if os.name == "posix" and settings.COMPRESSION == "lzma" and six.PY2:
        try:
            cmd = "XZ_OPT=-9 tar --directory=%s -Jcf %s %s" % (
                settings.RESULT_DIR,
                output_filename,
                dsetname,
            )
            check_output(cmd, stderr=STDOUT, shell=True)
        except CalledProcessError:
            error("There was an error executing '%s'.")
            raise SystemExit
    elif settings.COMPRESSION == "lzma" and six.PY2:
        error("lzma compression is not yet available for your platform.")
        raise SystemExit
    else:
        mode = "w:%s" % extension
        with tarfile.open(output_filename, mode, compresslevel=9) as tar:
            tar.add(dsetpath, arcname=os.path.basename(dsetpath))


def compress_results(task_dict):
    """Compress results for all datasets which are complete

    This function iterates over all datasets defined in the settings file, and
    collects a list of files in the result directory that correspond to each
    dataset. Next, for each dataset that is complete, the function
    :func:`compress_dataset` is called, which does the actual compressing.

    Parameters
    ----------
    task_dict : dict
        The dict with the mappings from hashes to command dicts, as returned by
        :func:`.tasks.init_tasks`.

    """
    completed_dsets = []
    for dset in settings.DATASETS:
        try:
            files = [f for f in files_w_dataset(dset)]
        except:
            continue
        if dataset_completed(files, dset, task_dict):
            completed_dsets.append(dset)

    info(
        "Starting compression of %i completed result directories."
        % len(completed_dsets)
    )
    for dset in iter_progress(completed_dsets, "Datasets"):
        compress_dataset(dset)
