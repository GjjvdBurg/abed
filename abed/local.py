
import shutil

from mpi4py import MPI

from abed.conf import settings
from abed.run_utils import get_scratchdir
from abed.utils import info, mkdir

def copy_local_files():
    rank = MPI.COMM_WORLD.Get_rank()
    if not rank == 0:
        return
    scratch = get_scratchdir(local=True)
    info('Creating local scratch dir: %s' % scratch)
    mkdir(scratch)
    scratch_data = '%s/%s' % (scratch, 'datasets')
    shutil.copytree(settings.DATADIR, scratch_data)
    info('Copying local data dir: %s' % scratch_data)
    scratch_exec = '%s/%s' % (scratch, 'execs')
    shutil.copytree(settings.EXECDIR, scratch_exec)
    info('Copying local exec dir: %s' % scratch_exec)
    scratch_results = '%s/%s' % (scratch, 'results')
    mkdir(scratch_results)
    info('Creating local scratch results dir: %s' % scratch_results)

