# -*- coding: utf-8 -*-

import os

from .conf import settings
from .io import info
from .utils import mkdir


def get_scratchdir(local=False):
    if local:
        return os.getcwd()
    if settings.REMOTE_SCRATCH:
        scratchdir = settings.REMOTE_SCRATCH
    else:
        scratchdir = os.getenv(settings.REMOTE_SCRATCH_ENV, ".")
    return scratchdir


def get_output_dir(result_dir, quiet=False):
    subdirs = os.listdir(result_dir)
    if not subdirs:
        outdir = "%s/0" % (result_dir)
        mkdir(outdir)
        if not quiet:
            info("Created result output dir %s" % outdir)
        return outdir
    latest = sorted(map(int, subdirs))[-1]
    files = os.listdir(result_dir + "/" + str(latest))
    if len(files) >= settings.MAX_FILES:
        outdir = "%s/%i" % (result_dir, latest + 1)
        mkdir(outdir)
        if not quiet:
            info("Created result output dir %s" % outdir)
    else:
        outdir = "%s/%i" % (result_dir, latest)
    return outdir


def write_output(output, hsh, local=False):
    scratchdir = get_scratchdir()
    if local:
        scratch_results = settings.STAGE_DIR
    else:
        scratch_results = "%s/results" % scratchdir
    mkdir(scratch_results)
    outdir = get_output_dir(scratch_results)
    fname = "%s/%s%s" % (outdir, hsh, settings.RESULT_EXTENSION)
    with open(fname, "w") as fid:
        fid.write(output)
    return fname
