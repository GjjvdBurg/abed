# -*- coding: utf-8 -*-


"""
Functions for managing tasks

"""

import os
import sys
import random
import hashlib

from itertools import product

from .conf import settings
from .exceptions import (
    AbedHashCollissionException,
    AbedExperimentTypeException,
)
from .results.walk import walk_hashes
from .io import error


def cartesian(params):
    return (dict(list(zip(params, x))) for x in product(*params.values()))


def check_size():
    if not sys.maxsize == 9223372036854775807:
        error("Running on a non 64-bit system. This may cause problems with " "hashes.")
        raise SystemExit


def task_hash(task):
    """
    This yields a hash of a list by combining the hashes of all list elements.
    """
    as_tuples = sorted(task.items())
    hasher = hashlib.blake2b(digest_size=8)
    for key, value in as_tuples:
        k = repr(key)
        v = repr(value)
        hasher.update(k.encode())
        hasher.update(v.encode())
    return hasher.hexdigest()


def init_tasks():
    if settings.TYPE in ["ASSESS_GRID", "ASSESS"]:
        task_func = init_tasks_assess_grid
    elif settings.TYPE == "ASSESS_LIST":
        task_func = init_tasks_assess_list
    elif settings.TYPE == "CV_TT":
        task_func = init_tasks_cv_tt
    elif settings.TYPE == "RAW":
        task_func = init_tasks_raw
    else:
        raise ValueError(f"Unknown TYPE value in settings: {settings.TYPE}")

    try:
        return task_func()
    except AbedHashCollissionException:
        error(
            "A hash collision occured. This rarely occurs naturally, so it"
            " is most likely caused by duplicate tasks in the task list. "
            "Abed does not currently support duplicate tasks."
        )
        raise SystemExit
    raise AbedExperimentTypeException


def init_tasks_assess_grid():
    out = {}
    for dset in settings.DATASETS:
        for method in settings.METHODS:
            for prmset in cartesian(settings.PARAMS[method]):
                task = {key: value for key, value in prmset.items()}
                task["dataset"] = dset
                task["method"] = method
                hsh = task_hash(task)
                if hsh in out:
                    raise AbedHashCollissionException
                out[hsh] = task
    return out


def init_tasks_assess_list():
    out = {}
    for dset in settings.DATASETS:
        for method in settings.METHODS:
            for prmset in settings.PARAMS[method]:
                task = {key: value for key, value in prmset.items()}
                task["dataset"] = dset
                task["method"] = method
                hsh = task_hash(task)
                if hsh in out:
                    raise AbedHashCollissionException
                out[hsh] = task
    return out


def init_tasks_cv_tt():
    out = {}
    rng = random.Random(x=settings.CV_BASESEED)
    for train, test in settings.DATASETS:
        seed = rng.randint(0, 2 ** 31 - 1)
        for method in settings.METHODS:
            for prmset in cartesian(settings.PARAMS[method]):
                task = {key: value for key, value in prmset.items()}
                task["train_dataset"] = train
                task["test_dataset"] = test
                task["method"] = method
                task["cv_seed"] = seed
                hsh = task_hash(task)
                if hsh in out:
                    raise AbedHashCollissionException
                out[hsh] = task
    return out


def init_tasks_raw():
    out = {}
    with open(settings.RAW_CMD_FILE, "r") as fid:
        tasks = [x.strip() for x in fid.readlines() if x.strip()]
    for txttask in tasks:
        hsh = hash(txttask)
        hsh %= (sys.maxsize + 1) * 2
        if hsh in out:
            raise AbedHashCollissionException
        out[hsh] = txttask
    return out


def read_tasks():
    with open(settings.TASK_FILE, "r") as fid:
        tasks = [l.strip() for l in fid.readlines() if l.strip()]
    grid = init_tasks()
    out = {}
    for key in tasks:
        out[key] = grid[key]
    return out


def update_tasks(tasks):
    delcnt = 0
    if not os.path.exists(settings.RESULT_DIR):
        return 0
    for hsh in walk_hashes():
        try:
            del tasks[hsh]
            delcnt += 1
        except KeyError:
            pass
    return delcnt


def explain_tasks(all_tasks):
    for task in sorted(all_tasks.keys()):
        if settings.TYPE == "RAW":
            cmd = all_tasks[task]
        else:
            d = {k: v for k, v in all_tasks[task].items()}
            command = settings.COMMANDS[d["method"]]
            d["datadir"] = "{datadir}"
            d["execdir"] = "{execdir}"
            cmd = command.format(**d)
        print("%s : %s" % (task, cmd))


def filter_tasks(all_tasks, query_words=None):
    """Keep only those tasks that match all words in the query list"""
    if query_words is None:
        return all_tasks

    keep = {}
    for task_id in all_tasks:
        task = all_tasks[task_id]
        if all(q in task_id for q in query_words):
            keep[task_id] = task.copy()
            continue

        # Match if all query words match some task value
        all_match = True
        for q in query_words:
            match = any(q in str(v) for v in task.values())
            if not match:
                all_match = False
                break

        if all_match:
            keep[task_id] = task.copy()

    return keep
