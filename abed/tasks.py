"""
Functions for managing tasks

"""

import os
import sys

from itertools import izip, product

from abed import settings
from abed.exceptions import AbedHashCollissionException
from abed.utils import error

def cartesian(params):
    return (dict(izip(params, x)) for x in product(*params.itervalues()))

def check_size():
    if not sys.maxsize == 9223372036854775807:
        error("Running on a non 64-bit system. This may cause problems with "
                "hashes.")
        raise SystemExit

def task_hash(task):
    """
    This yields a hash of a list by combining the hashes of all list elements.
    """
    hsh = hash(frozenset(task.items()))
    hsh %= ((sys.maxsize + 1) * 2)
    return hsh

def init_tasks():
    out = {}
    for dset in settings.DATASETS:
        for method in settings.METHODS:
            for prmset in cartesian(settings.PARAMS[method]):
                task = {key: value for key, value in prmset.iteritems()}
                task['dataset'] = dset
                task['method'] = method
                hsh = task_hash(task)
                if hsh in out:
                    raise AbedHashCollissionException
                out[hsh] = task
    return out

def read_tasks():
    with open(settings.TASK_FILE, 'r') as fid:
        tasks = fid.readlines()
    tasks = [x.strip() for x in tasks]
    tasks = map(int, tasks)
    grid = init_tasks()
    out = {}
    for key in tasks:
        out[key] = grid[key]
    return out

def update_tasks(tasks):
    delcnt = 0
    resdirs = os.listdir(settings.RESULT_DIR)
    for resdir in resdirs:
        files = os.listdir(resdir)
        for f in files:
            fname = os.path.basename(f)
            hsh = os.path.splitext(fname)[0]
            try:
                del tasks[int(hsh)]
                delcnt += 1
            except KeyError:
                pass
    return delcnt
