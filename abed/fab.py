"""Functions for using fabric

Abed uses Fabric to synchronize data to and from the compute cluster. The 
various functions that Abed needs are defined here. A helper class is defined 
in :mod:`fab_util`, which is used to define the Fabric context environment that 
is used for the commands.

"""

import os
import time

from fabric.operations import local
from tempfile import gettempdir

from .auto import get_jobid_from_logs
from .conf import settings
from .fab_util import myfab
from .pbs import generate_pbs_text
from .io import info
from .utils import mkdir


def init_data():
    """Push the data to the remote server

    This function is used to synchronize the :setting:`DATADIR` directory to
    the compute cluster. This is done by first locally compressing the entire
    directory as a tar file, then syncing it to a ``datasets`` directory in the
    remote project path, and unpacking it there. The path where the unpacked
    dataset is located is stored in the :class:`MyFabric` class.

    """
    local("tar czf datasets.tar.gz -C {} .".format(settings.DATADIR, os.sep))
    release_time = time.strftime("%s")
    release_path = "{ppath}/{datapath}/{relpath}".format(
        ppath=myfab.project_path, datapath="datasets", relpath=release_time
    )
    myfab.run("mkdir -p {releasepath}".format(releasepath=release_path))
    myfab.put("./datasets.tar.gz", release_path)
    myfab.run("cd {} && tar xvf datasets.tar.gz".format(release_path))
    myfab.run("cd {} && ".format(release_path, "datasets") + "rm datasets.tar.gz")
    local("rm datasets.tar.gz")
    info("Remote datasets placed in: {}".format(release_path))
    myfab.data_path = release_path


def move_data():
    """ Move the data from previous release """
    curr_path = "{}/releases/current".format(myfab.project_path)
    prev_path = "{}/releases/previous".format(myfab.project_path)
    myfab.run("mkdir -p {}/{}/".format(curr_path, "datasets"))
    myfab.run(
        "rsync -av --remove-source-files {}/{}/* {}/{}/".format(
            prev_path, "datasets", curr_path, "datasets"
        )
    )


def setup():
    myfab.run("mkdir -p {}".format(myfab.project_path))
    myfab.run("mkdir -p releases; mkdir -p packages;", cd=myfab.project_path)


def deploy(push_data=False):
    if push_data:
        assert not myfab.data_path is None

    # upload tar from git
    release_time = time.strftime("%Y_%m_%d_%H_%M_%S")
    sha1 = local("git log master -1 --pretty=format:'%h'", capture=True)
    release_name = "{}_{}".format(release_time, sha1)
    release_path = "{}/releases/{}".format(myfab.project_path, release_name)
    release_file_name = "{}_{}.tar.gz".format(release_time, sha1)
    package_file_path = "{}/packages/{}".format(myfab.project_path, release_file_name)
    # archive locally
    local("git archive --format=tar master | gzip > " "{}.tar.gz".format(release_name))
    myfab.run("mkdir " + release_path)
    # transfer to remote
    myfab.put(release_file_name, package_file_path)
    local("rm " + release_file_name)
    myfab.run("cd {} && tar zxf {}".format(release_path, package_file_path))

    # copy data if pushed
    if push_data:
        myfab.run("mkdir -p {}/{}/".format(release_path, "datasets"))
        myfab.run("cp {}/* {}/{}/".format(myfab.data_path, release_path, "datasets"))

    # symlinks
    if not push_data:
        myfab.run(
            "rm -f releases/previous; mv releases/current " "releases/previous",
            warn_only=True,
            cd=myfab.project_path,
        )
    myfab.run("ln -s {} releases/current".format(release_path), cd=myfab.project_path)


def get_files_from_glob(glob_path, glob, dest_dir):
    lstxt = myfab.run(
        "shopt -s nullglob && ls -1 %s && shopt -u nullglob" % glob,
        cd=glob_path,
    )
    files = [os.path.join(glob_path, f) for f in lstxt.split("\n")]
    for f in files:
        fname = os.path.basename(f)
        lpath = "%s%s%s" % (dest_dir, os.sep, fname)
        if not os.path.exists(lpath):
            myfab.get(f, dest_dir)


def get_results(basepath=None):
    if basepath is None:
        basepath = "{}/releases/current".format(myfab.project_path)

    zip_path = "{}/bzips".format(basepath)
    zip_glob = "*.tar.bz2"
    mkdir(settings.ZIP_DIR)
    get_files_from_glob(zip_path, zip_glob, settings.ZIP_DIR)

    log_path = "{}/logs".format(basepath)
    log_glob = "*"
    mkdir(settings.LOG_DIR)
    get_files_from_glob(log_path, log_glob, settings.LOG_DIR)


def write_and_queue():
    temp_pbs = os.path.join(gettempdir(), "abed.pbs")
    with open(temp_pbs, "w") as pbs:
        pbs.write(generate_pbs_text())
    curr_path = "{}/releases/current".format(myfab.project_path)
    myfab.put("/tmp/abed.pbs", "{}/".format(curr_path))
    myfab.run("mkdir -p {}/logs".format(curr_path))
    myfab.run("qsub -d . -e logs -o logs abed.pbs", cd=curr_path)
    local("rm /tmp/abed.pbs")


def build_remote():
    """
    Runs the build command remotely if the program requires compilation
    """
    if not settings.NEEDS_BUILD:
        return
    build_path = "{}/releases/current/{}".format(myfab.project_path, settings.BUILD_DIR)
    myfab.run(settings.BUILD_CMD, cd=build_path)


def fab_push():
    deploy(push_data=False)
    move_data()
    build_remote()
    write_and_queue()


def fab_pull():
    get_results()


def fab_setup():
    setup()
    init_data()
    deploy(push_data=True)


def fab_repull():
    releasepath = "{}/releases".format(myfab.project_path)
    lstext = myfab.run("ls -1 {}".format(releasepath))
    special = ["current", "previous"]
    paths = [x for x in lstext.split("\n") if not x in special]

    with open(settings.AUTO_FILE, "r") as fid:
        lines = fid.readlines()
    auto_jobids = [x.strip() for x in lines]

    to_pull = []
    for path in paths:
        fullpath = "{}/{}".format(releasepath, path)
        logpath = "{}/{}".format(fullpath, "logs")
        jobid = get_jobid_from_logs(logpath)
        if jobid in auto_jobids:
            to_pull.append(fullpath)

    for path in to_pull:
        zip_path = "{}/bzips/".format(path)
        zip_glob = "*.tar.bz2"
        mkdir(settings.ZIP_DIR)
        get_files_from_glob(zip_path, zip_glob, settings.ZIP_DIR)
