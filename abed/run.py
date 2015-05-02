"""
Functions for master/worker task execution

"""

import time

from mpi4py import MPI
from subprocess import check_output, CalledProcessError

from abed import settings
from abed.utils import info, error
from abed.run_utils import get_scratchdir, write_output

WORKTAG = 0
KILLTAG = 1

class Work(object):
    def __init__(self):
        self.work_items = []

    def get_next_item(self):
        if self.isempty():
            return None
        return self.work_items.pop()

    def isempty(self):
        return (len(self.work_items) == 0)

def get_work_chunk(all_work):
    next_work = []
    for n in range(settings.MW_SENDATONCE):
        next_work.append(all_work.get_next_item())
    next_work = [x for x in next_work if not x is None]
    if not next_work:
        next_work = None
    return next_work

def do_work(hsh, task):
    command = settings.COMMANDS[task['method']]
    task['datadir'] = '%s/%s' % (get_scratchdir(), settings.DATADIR)
    task['execdir'] = '%s/%s' % (get_scratchdir(), settings.EXECDIR)
    cmd = command.format(**task)
    try:
        print("Executing: '%s'" % cmd)
        output = check_output(cmd, shell=True)
    except CalledProcessError:
        error("There was an error executing: '%s'" % cmd)
    write_output(output, hsh)
    info("Finished with %s" % hsh)

def copy_worker():
    curdir = '%s/releases/current' % settings.REMOTE_PATH
    scratchdir = get_scratchdir()
    local_results = '%s/results/' % curdir
    scratch_results = '%s/results/' % scratchdir
    copy_task = ["rsync", "-avm", "--include='*.txt'", "-f", "'hide,!", " */i'", 
            scratch_results, local_results]
    while True:
        time.sleep(settings.MW_COPY_SLEEP)
        try:
            check_output(copy_task)
        except CalledProcessError:
            error("There was an error in the copy task")

def worker(task_dict):
    comm = MPI.COMM_WORLD
    status = MPI.Status()
    while True:
        hashes = comm.recv(obj=None, source=0, tag=MPI.ANY_TAG, status=status)
        if status.Get_tag() == KILLTAG:
            break
        for hsh in hashes:
            do_work(hsh, task_dict[hsh])
        comm.send(obj=None, dest=0)

def master(all_work):
    size = MPI.COMM_WORLD.Get_size()
    comm = MPI.COMM_WORLD
    status = MPI.Status()

    # send initial tasks to the workers
    for rank in range(2, size):
        next_work = get_work_chunk(all_work)
        comm.send(obj=next_work, dest=rank, tag=WORKTAG)

    # keep sending out tasks when requested
    while True:
        comm.recv(obj=None, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, 
                status=status)

        # if there is no more work we stop
        if all_work.isempty():
            break

        # otherwise, create a new work chunk for the worker
        next_work = get_work_chunk(all_work)
        comm.send(obj=next_work, dest=status.Get_source(), tag=WORKTAG)

    # collect all remaining results from workers that are still busy
    for rank in range(2, size):
        comm.recv(obj=None, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)

    # kill all worker processes
    for rank in range(2, size):
        comm.send(obj=None, dest=rank, tag=KILLTAG)

def mpi_start(task_dict):
    rank = MPI.COMM_WORLD.Get_rank()

    # 0 = master, 1 = copy, rest = worker
    if rank == 0:
        work = Work()
        work.work_items = task_dict.keys()
        master(work)
    elif rank == 1:
        copy_worker()
    else:
        worker(task_dict)
