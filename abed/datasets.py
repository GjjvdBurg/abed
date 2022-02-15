"""Helper functions for dealing with datasets

This file contains a helper function for dealing with dataset names.

"""


import os

from .conf import settings

basename = os.path.basename
splitext = os.path.splitext


def dataset_name(dset):
    """Get the dataset name for a given dataset

    The user has the option to specify alternative names for datasets in the
    :setting:`DATASETS` configuration setting, through the
    :setting:`DATASET_NAMES` variable. This function can be used to get the
    name of the dataset when the :setting:`DATASET_NAMES` variable is specified
    or not. If the setting is not specified, a name is created by stripping any
    extensions from the dataset specified. In case the dataset is a tuple, the
    names of the datasets are combined.

    Parameters
    ----------
    dset : str, tuple
        The dataset from the :setting:`DATASETS` configuration.

    Returns
    -------
    name : str
        The name of the dataset

    """

    if "DATASET_NAMES" in settings.__dict__:
        name = settings.DATASET_NAMES.get(dset, None)
        if not name is None:
            return name
    if isinstance(dset, tuple):
        txt = ""
        for name in dset:
            bname = basename(name)
            exts = splitext(bname)
            start = exts[0]
            txt += start + "_"
        txt = txt.rstrip("_")
    else:
        bname = basename(dset)
        exts = splitext(bname)
        start = exts[0]
        txt = start
    return txt
