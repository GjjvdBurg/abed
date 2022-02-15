"""Functions for automatic job management.

The functions in this module are used for automating the job management of PBS 
jobs. Abed has the ability to automatically submit a new job when a previous 
one is finished. To do this, functions are needed which check if any job is 
submitted, get the jobid of a running or finished job, get expected start times 
and remaining times, and mark finished jobs as done. This last functionality is 
needed to avoid repulling finished results.

"""

import os

from dateutil.parser import parse
from datetime import timedelta

from .conf import settings
from .exceptions import AbedPBSMultipleException
from .fab_util import myfab
from .io import info

RUNNING = "R"
QUEUED = "Q"


def submitted():
    """Check if a currently submitted job exists

    This function checks if a job exists on the remote, by trying to find a
    jobid from the pbs service. If no jobid can be found ``False`` is
    returned, otherwise ``True`` is returned. If a job exists, an attempt is
    made to check the state of the job, by through :func:`get_state`. If the
    job is queued, the starttime is retrieved through :func:`get_starttime`,
    and if it is running, the remaining time is retrieved through
    :func:`get_remaining`.

    Returns
    -------
    bool
        Whether or not a currently submitted job exists.

    """
    jobid = get_jobid_from_pbs()
    if jobid is None:
        return False
    state = get_state(jobid)
    if state == QUEUED:
        sttime = get_starttime(jobid)
        if sttime:
            info("Job %s queued. Start time: %s" % (jobid, sttime.strftime("%c")))
        else:
            info("Job %s queued." % jobid)
    elif state == RUNNING:
        rmtime = get_remaining(jobid)
        info("Job %s running. Time remaining: %s" % (jobid, rmtime))
    return True


def get_jobid_from_pbs():
    """Try to get the jobid of a running job from the PBS server

    This function attempts to get the jobid of a currently running job by 
    running the ``qstat`` command, and trying to find a line that looks similar 
    to this::

        9941363.batch1.lisa.su username queuename jobname SessID NDS TSK --\
        00:01:00 R 00:00:26

    From this line, it is assumed that the text before the first period is the 
    jobid, ``9941363`` in this case.

    Returns
    -------
    str
        The id of the job as text. None is returned if no job is found.

    Raises
    ------
    AbedPBSMultipleException
        When more than one job is running simultaneously, an exception is 
        thrown. In this case the program doesn't know which task to manage.

    """
    text = myfab.run(
        "qstat -u %s | grep %s | cut -d'.' -f1"
        % (settings.REMOTE_USER, settings.REMOTE_USER)
    )
    if not text:
        return None
    ids = text.split("\n")
    if len(ids) > 1:
        raise AbedPBSMultipleException
    return ids[0]


def get_jobid_from_logs(logpath=None):
    """Try to get the jobid from existing log files

    This function attempt to get the jobid of a finished job by checking the
    filenames of the log files. If used as expected, the PBS server will place
    output and error logs in the logs directory with the names
    ``abed.pbs.o{jobid}`` and ``abed.pbs.e{jobid}``. This function expects
    this exact format, and tries to retrieve the jobid from the first file in
    the logs directory.

    Parameters
    ----------
    logpath : str, optional
        An optional path to search for the log files. If not provided, the
        path ``{remote_dir}/releases/current/logs/`` will be used.

    Returns
    -------
    jobid : str
        The ID of the job that created the log files. None is returned when no
        jobid can be found.

    """
    if logpath is None:
        logpath = "%s/releases/current/logs/" % settings.REMOTE_DIR
    try:
        text = myfab.run("ls -1 %s" % logpath)
    except:
        return None
    if not text:
        return None
    try:
        jobid = text.split("\n")[0].split(".")[-1][1:]
    except:
        jobid = None
    return jobid


def get_state(jobid):
    """Get the state of the job with the provided jobid

    This function uses the PBS command ``qstat -f username`` to find out the
    state of the job. It is assumed that a job with the given jobid exists.
    See the documentation of the ``qstat`` command for possible job states.

    Parameters
    ----------
    jobid : str
        The PBS id of a job.

    Returns
    -------
    state : str
        The state of the job as given by the ``qstat`` command.

    """
    text = myfab.run("qstat -f %s | grep job_state | cut -d'=' -f2" % jobid)
    return text


def get_starttime(jobid):
    """Get the expected start time of a queued job

    This function tries to find the start time of a queued job by using the
    ``showstart`` command (assuming it is available). It is expected that the
    output of showstart contains a line of the form::

       Earliest start in          1:26:14 on Thu May 26 22:56:43

    From this string the date at the end is extracted, which is converted to a
    datetime.datetime object and returned.

    Parameters
    ----------
    jobid : str
        The PBS id of a job.

    Returns
    -------
    starttime : datetime.datetime
        The expected start time of the job as given by ``showstart``. None is
        returned if no date can be found.

    """
    text = myfab.run("showstart %s | grep start | cut -d'o' -f2- | cut -c 3-" % jobid)
    if not text.strip():
        return None
    try:
        timestr = parse(text)
    except:
        return None
    return timestr


def get_remaining(jobid):
    """Get the remaining runtime of a job

    This function uses the ``qstat -f`` command to retrieve the remaining
    walltime of the specified job. It does this by looking for the line::

        Walltime.Ramining = 32754

    and converting this to a string of the form ``HH:MM:SS`` through
    `datetime.timedelta`.

    Parameters
    ----------
    jobid : str
        The PBS id of a job.

    Returns
    -------
    str
        The remaining time for the specified job in the form HH:MM:SS.

    """
    text = myfab.run("qstat -f %s | grep Remaining | cut -d'=' -f2" % jobid)
    td = timedelta(0, int(text))
    return str(td)


def is_job_marked(jobid):
    """Check if a job is marked in the auto file

    This function checks if a given jobid occurs in the auto file. The auto
    file is used to record for which jobs the results have been pulled from
    the server. The auto file records the jobids one for each line (see
    :func:`mark_job`), so this function checks if the provided jobid is on any
    of the lines.

    Parameters
    ----------
    jobid : str
        The PBS id of a job.

    Returns
    -------
    bool
        Whether or not the job is marked in the auto file.

    """
    if not os.path.exists(settings.AUTO_FILE):
        return False
    with open(settings.AUTO_FILE, "r") as fid:
        lines = fid.readlines()
    ids = [x.strip() for x in lines]
    if jobid in ids:
        return True
    return False


def mark_job(jobid):
    """Mark the job in the auto file

    See also :func:`is_job_marked`. This function marks a job by appending the
    given jobid to the auto file.

    Parameters
    ----------
    jobid : str
        The PBS id of a job.

    """
    with open(settings.AUTO_FILE, "a") as fid:
        fid.write(jobid + "\n")
