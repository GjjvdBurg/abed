"""
Functions for dealing with git

"""

from subprocess import check_output, CalledProcessError

from abed import settings
from abed.utils import error, info

def git_init():
    # init repo
    try:
        check_output(['git', 'init'])
    except CalledProcessError:
        error("Error executing 'git init'")
        raise
    # add conf
    try:
        check_output(['git', 'add', 'abed_conf.py'])
    except CalledProcessError:
        error("Error executing 'git add abed_conf.py'")
        raise
    try:
        check_output(['git', 'commit' ,'-am', '"initialized abed skeleton"'])
    except CalledProcessError:
        error("Error executing initial commit")
        raise

def git_add_tbd():
    # add tbd
    try:
        check_output(['git', 'add', settings.TASK_FILE])
    except CalledProcessError:
        error("Error executing 'git add %s'" % settings.TASK_FILE)
        raise

def git_commit_tbd():
    try:
        check_output(['git', 'commit', '-m',
            '"automatic commit of TBD task file"', settings.TASK_FILE])
    except CalledProcessError:
        error("Error performing autocommit for TBD file")
        raise
    info("Automatic TBD file commit")
