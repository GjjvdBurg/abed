"""
Functions for dealing with Git

In this file functions are defined for dealing with the Git repository: 
creating the initial repository, committing changes to the task file or the 
auto file, and checking if the working directory is clean.

"""

from git import Repo

from .conf import settings
from .constants import CONFIG_FILENAME, TASKS_FILENAME, AUTO_FILENAME
from .io import info


def git_init():
    """Initializes the Git repository for Abed

    This function initializes a Git repository in the current directory, adds
    the task file, the auto file, and the settings file, and commits them to
    the Git repository.

    """
    repo = Repo.init(".")
    repo.index.add([CONFIG_FILENAME])
    repo.index.add([TASKS_FILENAME])
    repo.index.add([AUTO_FILENAME])
    repo.index.commit("initialized abed skeleton")


def git_commit_file(filename, message):
    """Commit changes to a given file if necessary

    This function commits changes to a given file to the git repository, using
    the provided message as the commit message. It also prints the message to
    the user with the :func:`info()` function, with the addition of the word
    "Git". Note that changes will only be committed if necessary.

    Parameters
    ----------
    filename : str
        The filename of the file to commit.
    message : str
        The commit message.

    """
    repo = Repo(".")
    diffidx = repo.index.diff(None, [filename])
    if not diffidx:
        return
    repo.index.add([filename])
    repo.index.commit(message)
    info("Git - " + message)


def git_commit_tbd():
    """Wrapper around :func:`git_commit_file()` for the TBD file """
    git_commit_file(settings.TASK_FILE, "Automatic commit of TBD task file")


def git_commit_auto():
    """Wrapper around :func:`git_commit_file()` for the auto file """
    git_commit_file(settings.AUTO_FILE, "Automatic commit of auto log file")


def git_ok():
    """Check if the Git working directory is clean"""
    repo = Repo(".")
    return not repo.is_dirty()
