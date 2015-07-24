"""
Functions for using fabric
"""

import os
import time

from fabric.operations import local

from abed import settings
from abed.auto import get_jobid_from_logs
from abed.fab_util import myfab
from abed.pbs import generate_pbs_text
from abed.utils import info, mkdir

def init_data():
    """ Push the data to the remote server """
    local('tar czf datasets.tar.gz {}{}*'.format(settings.DATADIR, os.sep))
    release_time = time.strftime('%s')
    release_path = '{ppath}/{datapath}/{relpath}'.format(
            ppath=myfab.project_path, datapath=settings.DATADIR, 
            relpath=release_time)
    myfab.run('mkdir -p {releasepath}'.format(releasepath=release_path))
    myfab.put('./datasets.tar.gz', release_path)
    myfab.run('cd {} && tar xvf datasets.tar.gz'.format(release_path))
    myfab.run('cd {} && mv {}/* . && '.format(release_path, settings.DATADIR) +
            'rm datasets.tar.gz && rm -r {}'.format(settings.DATADIR))
    local('rm datasets.tar.gz')
    info('Remote datasets placed in: {}'.format(release_path))
    myfab.data_path = release_path

def move_data():
    """ Move the data from previous release """
    curr_path = '{}/releases/current'.format(myfab.project_path)
    prev_path = '{}/releases/previous'.format(myfab.project_path)
    myfab.run('mkdir -p {}/{}/'.format(curr_path, settings.DATADIR))
    myfab.run('mv {}/{}/* {}/{}/'.format(prev_path, settings.DATADIR, curr_path, 
        settings.DATADIR))

def setup():
    myfab.run('mkdir -p {}'.format(myfab.project_path))
    myfab.run('mkdir -p releases; mkdir -p packages;', cd=myfab.project_path)

def deploy(push_data=False):
    if push_data:
        assert(not myfab.data_path is None)

    # upload tar from git
    release_time = time.strftime('%Y_%m_%d_%H_%M_%S')
    sha1 = local("git log master -1 --pretty=format:'%h'", capture=True)
    release_name = '{}_{}'.format(release_time, sha1)
    release_path = '{}/releases/{}'.format(myfab.project_path, release_name)
    release_file_name = '{}_{}.tar.gz'.format(release_time, sha1)
    package_file_path = '{}/packages/{}'.format(myfab.project_path,
            release_file_name)
    # archive locally
    local('git archive --format=tar master | gzip > '
            '{}.tar.gz'.format(release_name))
    myfab.run('mkdir ' + release_path)
    # transfer to remote
    myfab.put(release_file_name, package_file_path)
    local('rm ' + release_file_name)
    myfab.run('cd {} && tar zxf {}'.format(release_path, package_file_path))

    # copy data if pushed
    if push_data:
        myfab.run('mkdir -p {}/{}/'.format(release_path, settings.DATADIR))
        myfab.run('cp {}/* {}/{}/'.format(myfab.data_path, release_path, 
            settings.DATADIR))

    # symlinks
    if not push_data:
        myfab.run('rm -f releases/previous; mv releases/current '
                'releases/previous', warn_only=True, cd=myfab.project_path)
    myfab.run('ln -s {} releases/current'.format(release_path), 
            cd=myfab.project_path)

def get_files_from_glob(glob, dest_dir):
    lstxt = myfab.run('ls -1 %s' % glob)
    files = lstxt.split('\n')
    for f in files:
        fname = os.path.basename(f)
        lpath = '%s%s%s' % (dest_dir, os.sep, fname)
        if not os.path.exists(lpath):
            myfab.get(f, dest_dir)

def get_results(basepath=None):
    if basepath is None:
        basepath = '{}/releases/current'.format(myfab.project_path)

    zip_glob = '{}/bzips/*.tar.bz2'.format(basepath)
    mkdir(settings.ZIP_DIR)
    get_files_from_glob(zip_glob, settings.ZIP_DIR)

    log_glob = '{}/logs/*'.format(basepath)
    mkdir(settings.LOG_DIR)
    get_files_from_glob(log_glob, settings.LOG_DIR)

def write_and_queue():
    with open('/tmp/abed.pbs', 'w') as pbs:
        pbs.write(generate_pbs_text())
    curr_path = '{}/releases/current'.format(myfab.project_path)
    myfab.put('/tmp/abed.pbs', '{}/'.format(curr_path))
    myfab.run('mkdir -p {}/logs'.format(curr_path))
    myfab.run('qsub -d . -e logs -o logs abed.pbs', cd=curr_path)
    local('rm /tmp/abed.pbs')

def fab_push():
    deploy(push_data=False)
    move_data()
    write_and_queue()

def fab_pull():
    get_results()

def fab_setup():
    setup()
    init_data()
    deploy(push_data=True)

def fab_repull():
    releasepath = '{}/releases'.format(myfab.project_path)
    lstext = myfab.run('ls -1 {}'.format(releasepath))
    special = ['current', 'previous']
    paths = [x for x in lstext.split('\n') if not x in special]

    with open(settings.AUTO_FILE, 'r') as fid:
        lines = fid.readlines()
    auto_jobids = [x.strip() for x in lines]

    to_pull = []
    for path in paths:
        fullpath = '{}/{}'.format(releasepath, path)
        logpath = '{}/{}'.format(fullpath, 'logs')
        jobid = get_jobid_from_logs(logpath)
        if jobid in auto_jobids:
            to_pull.append(fullpath)

    for path in to_pull:
        zip_glob = '{}/bzips/*.tar.bz2'.format(path)
        mkdir(settings.ZIP_DIR)
        get_files_from_glob(zip_glob, settings.ZIP_DIR)
