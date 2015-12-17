
import os
import time

from abed.auto import submitted, get_jobid_from_logs, is_job_marked, mark_job
from abed.conf import settings
from abed.fab import fab_push, fab_pull, fab_repull, fab_setup
from abed.git import (git_add_auto, git_add_tbd, git_commit_auto, 
        git_commit_tbd, git_init, git_ok)
from abed.html.view import view_html
from abed.local import copy_local_files
from abed.results.main import make_results
from abed.run import mpi_start
from abed.skeleton import init_config
from abed.tasks import init_tasks, read_tasks, update_tasks
from abed.utils import info, error
from abed.zips import unpack_zips

class Abed(object):

    commands = [
            'auto',
            'explain_tasks',
            'local',
            'parse_results',
            'process_zips',
            'pull',
            'push',
            'reload_tasks',
            'repull',
            'run',
            'skeleton',
            'setup',
            'status',
            'update_tasks',
            'view_results'
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
            git_add_auto()
            git_add_tbd()
            git_commit_auto()
            git_commit_tbd()

    def explain_tasks(self):
        for task in sorted(self.task_dict.keys()):
            d = {k:v for k, v in self.task_dict[task].iteritems()}
            command = settings.COMMANDS[d['method']]
            d['datadir'] = '[datadir]'
            d['execdir'] = '[execdir]'
            cmd = command.format(**d)
            print('%s : %s' % (task, cmd))

    def update_tasks(self):
        # this takes over update_tasks
        cnt = update_tasks(self.task_dict)
        info("Task update removed %i completed tasks. Tasks remaining: %i" % 
                (cnt, len(self.task_dict)))
        self.write_tasks()
        git_commit_tbd()
        if len(self.task_dict) == 0:
            info("All tasks completed. Cool cool cool.")

    def reload_tasks(self):
        self.task_dict = init_tasks()
        self.update_tasks()

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

    def pull(self, jobid=None):
        info("Starting pull")
        fab_pull()
        info("Starting unpacking of zips")
        unpack_zips()
        if jobid is None:
            jobid = get_jobid_from_logs()
        info("Marking job as pulled: %s" % jobid)
        mark_job(jobid)
        git_commit_auto()
        info("Updating tasks")
        self.update_tasks()

    def auto(self):
        info("Starting auto loop")
        while True:
            if len(self.task_dict) == 0:
                info("Stopping auto loop")
                break
            if submitted() is None:
                info("No submitted task found, assuming done.")
                jobid = get_jobid_from_logs()
                info("Found jobid from logs: %s" % jobid)
                if not is_job_marked(jobid):
                    info("Job %s not pulled yet, pulling it" % jobid)
                    self.pull(jobid=jobid)
                if len(self.task_dict) == 0:
                    break
                info("Starting push")
                self.push()
            info("Task busy, sleeping for a while ...")
            time.sleep(settings.AUTO_SLEEP)
        info("Starting parse_results")
        self.parse_results()

    def parse_results(self):
        # this takes over parse_results.py
        info("Starting make_results()")
        make_results(self.task_dict)

    def run(self):
        # this takes over master/worker
        if self.task_dict is None:
            error("No tasks defined before attempted run. Exiting")
            raise SystemExit
        mpi_start(self.task_dict)
        info("Finished with run command.")

    def skeleton(self):
        init_config()
        git_init()

    def status(self):
        info("Number of tasks to be done: %i" % len(self.task_dict))

    def process_zips(self):
        unpack_zips()

    def repull(self):
        # use abed_auto.log to repull all zips from previous runs
        info("Starting repull based on {}".format(settings.AUTO_FILE))
        fab_repull()
        info("Unpacking zips")
        unpack_zips()
        info("Done repulling.")

    def view_results(self):
        view_html()

    def local(self):
        if self.task_dict is None:
            error("No tasks defined before attempted run. Exiting")
            raise SystemExit
        copy_local_files()
        mpi_start(self.task_dict, local=True)
        info("Finished with run command.")
