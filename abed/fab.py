"""
Functions for using fabric
"""

import time

from fabric.api import env
from fabric.context_managers import cd
from fabric.context_managers import settings as fab_settings
from fabric.operations import run, local, put, get

from abed import settings
from abed.pbs import generate_pbs_text

class MyFabric(object):
    """
    Class to manage env etc.
    """
    def __init__(self):
        self.host = settings.REMOTE_HOST
        self.user = settings.REMOTE_USER
        self.name = settings.PROJECT_NAME
        self.environment = 'staging'
        self.project_path = settings.REMOTE_PATH
        self.port = settings.REMOTE_PORT
        self.data_path = None

    def run(self, command=''):
        env.host_string = '%s@%s:%s' % (self.user, self.host, self.port)
        run(command)

    def get(self, source):
        env.host_string = '%s@%s:%s' % (self.user, self.host, self.port)
        get(source)

    def put(self, source, dest):
        env.host_string = '%s@%s:%s' % (self.user, self.host, self.port)
        put(source, dest)

def init_data(myfab):
    """ Push the data to the remote server """
    local('tar czf datasets.tar.gz datasets/*')
    release_time = time.strftime('%s')
    myfab.run('mkdir -p {}/datasets/{}'.format(myfab.project_path, 
        release_time))
    release_path = '{}/datasets/{}'.format(myfab.project_path, release_time)
    myfab.put('./datasets.tar.gz', release_path)
    myfab.run('cd {} && tar xvf datasets.tar.gz'.format(release_path))
    myfab.run('cd {} && mv datasets/* . && '.format(release_path) +
            'rm datasets.tar.gz && rm -r datasets')
    local('rm datasets.tar.gz')
    print('Datasets placed in: {}'.format(release_path))
    myfab.data_path = release_path

def move_data(myfab):
    """ Move the data from previous release """
    curr_path = '{}/releases/current/'.format(myfab.project_path)
    prev_path = '{}/releases/previous/'.format(myfab.project_path)
    myfab.run('mkdir -p {}datasets/'.format(curr_path))
    myfab.run('mv {}datasets/* {}datasets/'.format(prev_path, curr_path))

def setup(myfab):
    myfab.run('mkdir -p {}'.format(myfab.project_path))
    with (cd(myfab.project_path)):
        myfab.run('mkdir -p releases; mkdir -p packages;')

def deploy(myfab, push_data=False):
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
        myfab.run('mkdir -p {}/datasets/'.format(release_path))
        myfab.run('cp {}/* {}/datasets/'.format(myfab.data_path, release_path))

    # symlinks
    with (cd(myfab.project_path)):
        with fab_settings(warn_only=True):
            myfab.run('rm releases/previous; '
                    'mv releases/current releases/previous')
        myfab.run('ln -s {} releases/current'.format(release_path))

def get_results(myfab):
    myfab.get('{}/releases/current/bzips/*.tar.bz2'.format(myfab.project_path), 
            settings.ZIP_DIR)
    myfab.get('{}/releases/current/logs/*'.format(myfab.project_path), 
            settings.LOG_DIR)

def write_and_queue(myfab):
    with open('/tmp/abed.pbs', 'w') as pbs:
        pbs.write(generate_pbs_text())
    myfab.put('/tmp/abed.pbs', 
            '{}/releases/current/'.format(myfab.project_path))
    with (cd(myfab.project_path)):
        myfab.run('qsub -d . -e logs -o logs abed.pbs')
    local('rm /tmp/abed.pbs')

def fab_push():
    myfab = MyFabric()
    move_data(myfab)
    deploy(myfab, False)
    write_and_queue(myfab)

def fab_pull():
    myfab = MyFabric()
    get_results(myfab)

def fab_setup():
    myfab = MyFabric()
    setup(myfab)
    init_data(myfab)
    deploy(myfab, True)
