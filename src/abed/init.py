"""
Functions for creating a skeleton config file

"""

from abed.utils import info, mkdir

def init_config():
    txt = """
##############################################################################
#                                General Settings                            #
##############################################################################
PROJECT_NAME = ''
TASK_FILE = './abed_tasks.txt'
AUTO_FILE = './abed_auto.txt'
RESULT_DIR = '/path/to/local/results'
STAGE_DIR = '/path/to/local/stagedir'
MAX_FILES = 1000
ZIP_DIR = './zips'
LOG_DIR = './logs'
OUTPUT_DIR = './output'
AUTO_SLEEP = 120
HTML_PORT = 8000

##############################################################################
#                          Server parameters and settings                    #
##############################################################################
REMOTE_NEEDS_INIT = True
REMOTE_USER = 'username'
REMOTE_HOST = 'address.of.host'
REMOTE_DIR = '/home/%s/projects/project_name' % REMOTE_USER
REMOTE_PORT = 22
REMOTE_SCRATCH = None
REMOTE_SCRATCH_ENV = 'TMPDIR'

##############################################################################
#                      Settings for Master/Worker program                    #
##############################################################################
MW_SENDATONCE = 100 # number of tasks (hashes!) to send at once
MW_COPY_SLEEP = 120

##############################################################################
#                               Experiment type                              #
##############################################################################
# Uncomment the desired type
# Model assessment #
#TYPE = 'ASSESS'

# Cross validation with train and test dataset #
#TYPE = 'CV_TT'
#CV_BASESEED = 123456

##############################################################################
#                                Build settings                              #
##############################################################################
NEEDS_BUILD = False    # If remote compilation is required
BUILD_DIR = 'build'    # Relative directory where build takes place
BUILD_CMD = 'make all' # Build command

##############################################################################
#                      Experiment parameters and settings                    #
##############################################################################
DATADIR = 'datasets'
EXECDIR = 'execs'
DATASETS = ['dataset_1', 'dataset_2']
METHODS = ['method_1', 'method_2']
PARAMS = {
        'method_1': {
            'param_1': [val_1, val_2],
            'param_2': [val_3, val_4],
            'param_3': [val_5, val_6]
            },
        'method_2': {
            'param_1': [val_1, val_2, val_3],
            },
        }

COMMANDS = {
        'method_1': ("{execdir}/method_1 {datadir}/{dataset} {param_1} "
            "{param_2} {param_3}"),
        'method_2': "{execdir}/method_2 {datadir}/{dataset} {param_1}"
        }

METRICS = {
        'NAME_1': {
            'metric': metric_function_1,
            'best': max
            },
        'NAME_2': {
            'metric': metric_function_2,
            'best': min
            }
        }

SCALARS = {
        'time': {
            'best': min
            },
        }

RESULT_PRECISION = 4

DATA_DESCRIPTION_CSV = None

###############################################################################
#                                PBS Settings                                 #
###############################################################################
PBS_NODES = 1
PBS_WALLTIME = 360   # Walltime in minutes
PBS_CPUTYPE = None
PBS_CORETYPE = None
PBS_PPN = None
PBS_MODULES = ['mpicopy', 'python/2.7.9']
PBS_EXPORTS = ['PATH=$PATH:/home/%s/.local/bin/abed' % REMOTE_USER]
PBS_MPICOPY = ['datasets', 'execs', TASK_FILE]
PBS_TIME_REDUCE = 600 # Reduction of runtime in seconds

"""
    configfile = './abed_conf.py'
    with open(configfile, 'w') as fid:
        fid.write(txt)
    info("Wrote initial config to %s." % configfile)
    mkdir('datasets')
    mkdir('execs')
    info("Created 'datasets' and 'execs' directories")
