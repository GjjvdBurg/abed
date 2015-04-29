"""
Functions for automatic job management

"""

from dateutil.parser import parse

from abed import settings
from abed.exceptions import AbedPBSMultipleException
from abed.fab import MyFabric
from abed.utils import info

RUNNING = 'R'
QUEUED = 'Q'

def submitted():
    jobid = get_jobid_from_pbs()
    if jobid is None:
        return None
    state = get_state(jobid)
    if state == QUEUED:
        sttime = get_starttime()
        if sttime:
            info("Job %s queued. Start time: %s" % (jobid, 
                sttime.strftime("c")))
        else:
            info("Job %s queued.")
    elif state == RUNNING:
        rmtime = get_remaining()
        info("Jobf %s running. Time remaining: %s" % (jobid, 
            rmtime.strftime("%H:%M:%S")))

def get_jobid_from_pbs():
    myfab = MyFabric()
    empty = str(myfab.run("echo"))
    output = str(myfab.run("qstat -u %s | grep batch | tail -n +2 | "
        "cut -d'.' -f1" % settings.REMOTE_USER))
    text = output[len(empty)+1:].replace('\r', '').strip()
    ids = text.split('\n')
    if len(ids) > 1:
        raise AbedPBSMultipleException
    return ids[0]

def get_jobid_from_logs():
    logpath = '%s/releases/current/logs/' % settings.REMOTE_PATH
    myfab = MyFabric()
    empty = str(myfab.run("echo"))
    output = str(myfab.run("ls %s" % logpath))
    text = output[len(empty)+1:].replace('\r', '').strip()
    if text:
        return None
    jobid = text.split('\n')[0].split('.')[-1][1:]
    return jobid

def get_state(jobid):
    myfab = MyFabric()
    empty = str(myfab.run("echo"))
    output = str(myfab.run("qstat -f %s | grep job_state | cut -d'=' -f2" % 
        jobid))
    text = output[len(empty)+1:].replace('\r', '').strip()
    return text

def get_starttime(jobid):
    myfab = MyFabric()
    empty = str(myfab.run("echo"))
    output = str(
            myfab.run("showstart %s | grep start | cut -d'o' -f2- | cut -c 3-" % 
                jobid))
    text = output[len(empty)+1:].replace('\r', '').strip()
    return parse(text)

def get_remaining(jobid):
    myfab = MyFabric()
    empty = str(myfab.run("echo"))
    output = str(myfab.run("qstat -f %s | grep Remaining | cut -d'=' -f2" % 
        jobid))
    text = output[len(empty):].replace('\r', '').lstrip('\n').strip()
    return parse(text)
