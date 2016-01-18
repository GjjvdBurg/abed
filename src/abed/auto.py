"""
Functions for automatic job management

"""

import os

from dateutil.parser import parse
from datetime import timedelta

from abed.conf import settings
from abed.exceptions import AbedPBSMultipleException
from abed.fab_util import myfab
from abed.utils import info

RUNNING = 'R'
QUEUED = 'Q'

def submitted():
    jobid = get_jobid_from_pbs()
    if jobid is None:
        return None
    state = get_state(jobid)
    if state == QUEUED:
        sttime = get_starttime(jobid)
        if sttime:
            info("Job %s queued. Start time: %s" % (jobid, 
                sttime.strftime("%c")))
        else:
            info("Job %s queued.")
    elif state == RUNNING:
        rmtime = get_remaining(jobid)
        info("Job %s running. Time remaining: %s" % (jobid, rmtime))
    return True

def get_jobid_from_pbs():
    text = myfab.run("qstat -u %s | grep batch | tail -n +2 | "
        "cut -d'.' -f1" % settings.REMOTE_USER)
    if not text:
        return None
    ids = text.split('\n')
    if len(ids) > 1:
        raise AbedPBSMultipleException
    return ids[0]

def get_jobid_from_logs(logpath=None):
    if logpath is None:
        logpath = '%s/releases/current/logs/' % settings.REMOTE_DIR
    try:
        text = myfab.run("ls -1 %s" % logpath)
    except:
        return None
    if not text:
        return None
    jobid = text.split('\n')[0].split('.')[-1][1:]
    return jobid

def get_state(jobid):
    text = myfab.run("qstat -f %s | grep job_state | cut -d'=' -f2" % jobid)
    return text

def get_starttime(jobid):
    text = myfab.run("showstart %s | grep start | cut -d'o' -f2- | cut -c 3-" % 
            jobid)
    if not text.strip():
        return None
    return parse(text)

def get_remaining(jobid):
    text = myfab.run("qstat -f %s | grep Remaining | cut -d'=' -f2" % jobid)
    td = timedelta(0, int(text))
    return str(td)

def is_job_marked(jobid):
    if not os.path.exists(settings.AUTO_FILE):
        return False
    with open(settings.AUTO_FILE, 'r') as fid:
        lines = fid.readlines()
    ids = [x.strip() for x in lines]
    if jobid in ids:
        return True
    return False

def mark_job(jobid):
    with open(settings.AUTO_FILE, 'a') as fid:
        fid.write(jobid + '\n')
