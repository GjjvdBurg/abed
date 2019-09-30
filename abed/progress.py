# -*- coding: utf-8 -*-

"""
Functions for progress bars

"""

from tqdm import tqdm


def iter_progress(iterable, label=""):
    return tqdm(iterable, desc=label, leave=True)


def enum_progress(iterable, label=""):
    return enumerate(tqdm(iterable, desc=label, leave=True))
