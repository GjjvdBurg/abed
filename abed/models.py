
import os

from abed import settings
from abed.auto import submitted, get_jobid_from_logs
from abed.fab import fab_push, fab_pull, fab_setup
from abed.git import git_add_tbd, git_commit_tbd, git_init, git_ok
from abed.run import mpi_start
from abed.skeleton import init_config
from abed.tasks import init_tasks, read_tasks, update_tasks
from abed.utils import info, error
from abed.zips import unpack_zips

class Abed(object):

    commands = [
            'run',
            'push',
            'pull',
            'auto',
            'parse_results',
            'update_tasks',
            'skeleton',
            'setup',
            'status',
            ]

    def __init__(self):
        self.task_dict = None
        if not settings is None:
            self.init_tasks()

    def init_tasks(self):
        # this takes over init_tasks
        if os.path.isfile(settings.TASK_FILE):
            self.task_dict = read_tasks()
        else:
            self.task_dict = init_tasks()
            self.write_tasks()
            git_add_tbd()
            git_commit_tbd()

    def update_tasks(self):
        # this takes over update_tasks
        cnt = update_tasks(self.task_dict)
        info("Task update removed %i completed tasks. Tasks remaining: %i" % 
                (cnt, len(self.task_dict)))
        self.write_tasks()
        git_commit_tbd()

    def write_tasks(self):
        with open(settings.TASK_FILE, 'w') as fid:
            for task in sorted(self.task_dict.keys()):
                fid.write('%s\n' % task)
        info("Written task file to %s" % settings.TASK_FILE)

    def setup(self):
        info("Starting setup")
        fab_setup()

    def push(self):
        if not git_ok():
            error("Git repository has uncommitted changes, not pushing.")
            raise SystemExit
        info("Starting push")
        fab_push()

    def pull(self):
        info("Starting pull")
        fab_pull()
        unpack_zips()
        self.update_tasks()
        git_commit_tbd()

    def auto(self):
        # this takes over auto push pull
        while True:
            if not self.has_tasks():
                break
            if submitted() is None:
                jobid = get_jobid_from_logs()
                if not self.isprocessed(jobid):
                    self.pull()
                    self.push()
                    self.log_jobid(jobid)
        info("No more tasks left to be done")

    def parse_results(self):
        # this takes over parse_results.py
        pass

    def run(self):
        # this takes over master/worker
        mpi_start(self.task_dict)

    def skeleton(self):
        init_config()
        git_init()

    def status(self):
        print("abed number of tasks to be done: %i" % len(self.task_dict))
