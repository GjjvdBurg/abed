"""
Functions for dealing with git

"""

from subprocess import check_output, CalledProcessError

from .conf import settings
from .constants import CONFIG_FILENAME, TASKS_FILENAME, AUTO_FILENAME
from .utils import error, info

def git_init():
    # init repo
    try:
        check_output(['git', 'init'])
    except CalledProcessError as err:
        error("Error executing 'git init'. Error message:")
        print(err.output)
        raise SystemExit
    # add conf
    try:
        check_output(['git', 'add', CONFIG_FILENAME])
    except CalledProcessError as err:
        error("Error executing 'git add %s'. Error message:" %
                CONFIG_FILENAME)
        print(err.output)
        raise SystemExit
    try:
        check_output(['git', 'add', TASKS_FILENAME])
    except CalledProcessError as err:
        error("Error executing 'git add %s'. Error message:" % TASKS_FILENAME)
        print(err.output)
        raise SystemExit
    try:
        check_output(['git', 'add', AUTO_FILENAME])
    except CalledProcessError as err:
        error("Error executing 'git add %s'. Error message:" % AUTO_FILENAME)
        print(err.output)
        raise SystemExit
    try:
        check_output(['git', 'commit' ,'-am', 'initialized abed skeleton'])
    except CalledProcessError as err:
        error("Error executing initial commit. Error message:")
        print(err.output)
        raise SystemExit

def git_add_auto():
    try:
        check_output(['git', 'add', settings.AUTO_FILE])
    except CalledProcessError as err:
        error("Error executing 'git add %s'. Error message:" %
                settings.AUTO_FILE)
        print(err.output)
        raise SystemExit

def git_add_tbd():
    # add tbd
    try:
        check_output(['git', 'add', settings.TASK_FILE])
    except CalledProcessError as err:
        error("Error executing 'git add %s'. Error message:" %
                settings.TASK_FILE)
        print(err.output)
        raise SystemExit

def git_commit_tbd():
    try:
        check_output(['git', 'commit', '-m',
            'automatic commit of TBD task file', settings.TASK_FILE])
    except CalledProcessError as err:
        error("Error performing autocommit for TBD file. Error message:")
        print(err.output)
        raise SystemExit
    info("Automatic TBD file commit")

def git_commit_auto():
    try:
        check_output(['git', 'commit', '-m',
            'automatic commit of auto log file', settings.AUTO_FILE])
    except CalledProcessError as err:
        error("Error performing autocommit for auto log file. Error message:")
        print(err.output)
        raise SystemExit
    info("Automatic auto log file commit")

def git_ok():
    try:
        check_output(['git', 'diff', '--exit-code'])
    except CalledProcessError as err:
        if err.returncode == 1:
            return False
        error("Error performing 'git diff --exit-code'. Error message:")
        print(err.output)
        raise SystemExit
    return True
