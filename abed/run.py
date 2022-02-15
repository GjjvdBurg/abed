"""
Functions for master/worker task execution

"""

import datetime
import os
import time

from mpi4py import MPI
from subprocess import check_output, CalledProcessError

from .conf import settings
from .io import info, error
from .run_utils import get_scratchdir, write_output

WORKTAG = 0
KILLTAG = 1


class Work(object):
    def __init__(self, n_workers=1):
        self.work_items = []
        self.n_workers = n_workers

    def get_next_item(self):
        if self.isempty():
            return None
        return self.work_items.pop()

    def isempty(self):
        return len(self.work_items) == 0

    @property
    def send_at_once(self):
        if self.n_workers * settings.MW_SENDATONCE <= len(self.work_items):
            return settings.MW_SENDATONCE
        else:
            return 1

    def get_chunk(self):
        next_work = []
        for n in range(self.send_at_once):
            next_work.append(self.get_next_item())
        next_work = [x for x in next_work if not x is None]
        if not next_work:
            next_work = None
        return next_work


def do_work(hsh, task, local=False):
    datadir = os.path.join(get_scratchdir(local), "datasets")
    execdir = os.path.join(get_scratchdir(local), "execs")
    if settings.TYPE == "RAW":
        cmd = task.format(datadir=datadir, execdir=execdir)
    else:
        command = settings.COMMANDS[task["method"]]
        task["datadir"] = datadir
        task["execdir"] = execdir
        cmd = command.format(**task)
    dstr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        info("[%s] Executing: '%s'" % (dstr, cmd))
        output = check_output(cmd, shell=True)
        output = output.decode("utf-8")
    except CalledProcessError as err:
        error(
            "There was an error executing: '%s'. Here is the error: %s"
            % (cmd, err.output.decode("utf-8"))
        )
        return
    fname = write_output(output, hsh, local=local)
    dstr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    info("[%s] Written output of %s to file: %s" % (dstr, hsh, fname))


def copy_worker(local):
    comm = MPI.COMM_WORLD
    status = MPI.Status()
    scratchdir = get_scratchdir(local)
    curdir = "%s/releases/current" % settings.REMOTE_DIR
    local_results = "%s/results/" % curdir
    scratch_results = "%s/results/" % scratchdir
    logfile = "%s/logs/rsync.log" % curdir
    copy_task = "rsync -rtvu --delete --log-file=%s %s %s" % (
        logfile,
        scratch_results,
        local_results,
    )
    while True:
        if comm.Iprobe(source=0, tag=MPI.ANY_TAG):
            comm.recv(buf=None, source=0, tag=MPI.ANY_TAG, status=status)
            if status.Get_tag() == KILLTAG:
                break
        try:
            check_output(copy_task, shell=True)
        except CalledProcessError:
            error("There was an error in the copy task")
        time.sleep(settings.MW_COPY_SLEEP)


def worker(task_dict, local=False):
    comm = MPI.COMM_WORLD
    status = MPI.Status()
    while True:
        hashes = comm.recv(buf=None, source=0, tag=MPI.ANY_TAG, status=status)
        if status.Get_tag() == KILLTAG:
            break
        for hsh in hashes:
            do_work(hsh, task_dict[hsh], local=local)
        comm.send(obj=None, dest=0)


def master(all_work, worker_ranks, local=False):
    comm = MPI.COMM_WORLD
    status = MPI.Status()
    killed_workers = []

    # send initial tasks to the workers, if there is no work for a worker then
    # kill it
    for rank in worker_ranks:
        next_work = all_work.get_chunk()
        if next_work is None:
            killed_workers.append(rank)
            comm.send(obj=None, dest=rank, tag=KILLTAG)
        else:
            comm.send(obj=next_work, dest=rank, tag=WORKTAG)

    # keep sending out tasks when requested
    while True:
        comm.recv(buf=None, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)

        # if there is no more work we kill the source worker and break the loop
        if all_work.isempty():
            comm.send(obj=None, dest=status.Get_source(), tag=KILLTAG)
            killed_workers.append(status.Get_source())
            break

        # otherwise, create a new work chunk for the worker
        next_work = all_work.get_chunk()
        if next_work is None:
            continue
        comm.send(obj=next_work, dest=status.Get_source(), tag=WORKTAG)

    # collect all remaining results from workers that are still busy
    # we're using a non-blocking receive here (through Iprobe), so that we kill
    # worker processes as soon as possible.
    remaining = [r for r in worker_ranks if not r in killed_workers]
    while remaining:
        for rank in remaining:
            if comm.Iprobe(source=rank, tag=MPI.ANY_TAG):
                comm.recv(buf=None, source=rank, tag=MPI.ANY_TAG)
                comm.send(obj=None, dest=rank, tag=KILLTAG)
                killed_workers.append(rank)
        remaining = [r for r in worker_ranks if not r in killed_workers]

    # if we're here, there are no more tasks and all workers are killed, except
    # the copy worker. We'll give him a chance to complete and then quit.
    if settings.MW_COPY_WORKER and (not local):
        time.sleep(settings.MW_COPY_SLEEP)
        comm.send(obj=None, dest=1, tag=KILLTAG)


def mpi_start(task_dict, local=False):
    if local:
        mpi_start_local(task_dict)
    else:
        mpi_start_remote(task_dict)


def mpi_start_remote(task_dict):
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()

    # determine the true number of workers
    if settings.MW_NUM_WORKERS is None:
        if settings.MW_COPY_WORKER:
            n_workers = size - 2
        else:
            n_workers = size - 1
    else:
        n_workers = settings.MW_NUM_WORKERS

    # ranks of the worker processes
    worker_ranks = [r + 1 + settings.MW_COPY_WORKER for r in range(n_workers)]

    # 0 = master, 1 = copy, rest = worker
    if rank == 0:
        work = Work(n_workers=n_workers)
        work.work_items = list(task_dict.keys())
        master(work, worker_ranks)
    elif settings.MW_COPY_WORKER and rank == 1:
        copy_worker(local=False)
    elif rank in worker_ranks:
        worker(task_dict, local=False)


def mpi_start_local(task_dict):
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()

    # determine the true number of workers
    if settings.MW_NUM_WORKERS is None:
        n_workers = size - 1
    else:
        n_workers = settings.MW_NUM_WORKERS

    # ranks of the worker processes
    worker_ranks = [r + 1 + settings.MW_COPY_WORKER for r in range(n_workers)]

    # 0 = master, 1 = copy, rest = worker
    if rank == 0:
        work = Work(n_workers=n_workers)
        work.work_items = list(task_dict.keys())
        master(work, worker_ranks, local=True)
    elif rank in worker_ranks:
        worker(task_dict, local=True)
