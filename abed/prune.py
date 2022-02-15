# -*- coding: utf-8 -*-

"""Functionality for removing results that don't match the current config

"""

import os
import shutil

from pathlib import Path

from .conf import settings
from .utils import hash_from_filename, mkdir


def prune_results(task_dict, dry_run=False):
    """Remove result files that are not in the task_dict

    This can occur when the experiment configuration changes over time and old
    result files are still lying around. This command moves them to the
    PRUNE_DIR defined in the settings file.
    """
    if not os.path.exists(settings.RESULT_DIR):
        # no results, no pruning
        return

    # map from hash to Path of the result file
    tasks_have = {}

    dset_dirs = os.listdir(settings.RESULT_DIR)
    for dset in dset_dirs:
        dset_path = os.path.join(settings.RESULT_DIR, dset)

        method_dirs = os.listdir(dset_path)
        for method in method_dirs:
            method_path = os.path.join(dset_path, method)

            task_files = os.listdir(method_path)
            for filename in task_files:
                pth = os.path.join(method_path, filename)
                h = hash_from_filename(pth)
                tasks_have[h] = Path(pth)

    # list hashes that we don't have in the task dict
    unknown_hashes = []
    for h in tasks_have:
        if not h in task_dict:
            unknown_hashes.append(h)

    # no unknown hashes, no problem
    if not unknown_hashes:
        return

    # create the pruned dir if needed
    if not dry_run:
        mkdir(settings.PRUNE_DIR)

    # move the stragglers
    for h in unknown_hashes:
        path = tasks_have[h]
        filename = path.parts[-1]
        method = path.parts[-2]
        dset = path.parts[-3]

        dest_dir = os.path.join(settings.PRUNE_DIR, dset, method)
        if not dry_run:
            mkdir(dest_dir)

        dest_path = os.path.join(dest_dir, filename)
        it = 1
        while os.path.exists(dest_path):
            stem, ext = os.path.splitext(dest_path)
            filename = "%s_dup_%i%s" % (stem, it, ext)
            dest_path = os.path.join(dest_dir, filename)
            it += 1

        if dry_run:
            print("Moving %s to %s" % (path, dest_path))
        else:
            shutil.move(path, dest_path)
