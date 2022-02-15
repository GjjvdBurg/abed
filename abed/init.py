"""
Functions for creating a skeleton config file

"""

import os

from .constants import (
    CONFIG_FILENAME,
    DATASET_DIRNAME,
    EXECS_DIRNAME,
    TASKS_FILENAME,
    AUTO_FILENAME,
)
from .io import info
from .utils import mkdir, touch


def init_config():
    txt = """
##############################################################################
#                                General Settings                            #
##############################################################################
PROJECT_NAME = ''
TASK_FILE = '{task_file}'
AUTO_FILE = '{auto_file}'
RESULT_DIR = '/path/to/local/results'
STAGE_DIR = '/path/to/local/stagedir'
PRUNE_DIR = '/path/to/local/prunedir'
MAX_FILES = 1000
ZIP_DIR = './zips'
LOG_DIR = './logs'
OUTPUT_DIR = './output'
AUTO_SLEEP = 120
HTML_PORT = 8000
COMPRESSION = 'bzip2'
RESULT_EXTENSION = '.txt'

##############################################################################
#                          Server parameters and settings                    #
##############################################################################
REMOTE_USER = 'username'
REMOTE_HOST = 'address.of.host'
REMOTE_DIR = '/home/%s/projects/%s' % (REMOTE_USER, PROJECT_NAME)
REMOTE_PORT = 22
REMOTE_SCRATCH = None
REMOTE_SCRATCH_ENV = 'TMPDIR'

##############################################################################
#                      Settings for Master/Worker program                    #
##############################################################################
MW_SENDATONCE = 100 # number of tasks (hashes!) to send at once
MW_COPY_WORKER = False
MW_COPY_SLEEP = 120
MW_NUM_WORKERS = None

##############################################################################
#                               Experiment type                              #
##############################################################################
# Uncomment the desired type
# Model assessment #
#TYPE = 'ASSESS_GRID' # or 'ASSESS_LIST'

# Cross validation with train and test dataset #
#TYPE = 'CV_TT'
#CV_BASESEED = 123456
#YTRAIN_LABEL = 'y_train'

# Commands defined in a text file #
#TYPE = 'RAW'
#RAW_CMD_FILE = '/path/to/file.txt'

##############################################################################
#                                Build settings                              #
##############################################################################
NEEDS_BUILD = False    # If remote compilation is required
BUILD_DIR = 'build'    # Relative directory where build takes place
BUILD_CMD = 'make all' # Build command

##############################################################################
#                      Experiment parameters and settings                    #
##############################################################################
DATADIR = '{data_dir}'
EXECDIR = '{exec_dir}'

DATASETS = ['dataset_1', 'dataset_2']
DATASET_NAMES = {{k:str(i) for i, k in enumerate(DATASETS)}}

METHODS = ['method_1', 'method_2']
PARAMS = {{
        'method_1': {{
            'param_1': [val_1, val_2],
            'param_2': [val_3, val_4],
            'param_3': [val_5, val_6]
            }},
        'method_2': {{
            'param_1': [val_1, val_2, val_3],
            }},
        }}

COMMANDS = {{
        'method_1': ("{{execdir}}/method_1 {{datadir}}/{{dataset}} {{param_1}} "
            "{{param_2}} {{param_3}}"),
        'method_2': "{{execdir}}/method_2 {{datadir}}/{{dataset}} {{param_1}}"
        }}

METRICS = {{
        'NAME_1': {{
            'metric': metric_function_1,
            'best': max
            }},
        'NAME_2': {{
            'metric': metric_function_2,
            'best': min
            }}
        }}

SCALARS = {{
        'time': {{
            'best': min
            }},
        }}

RESULT_PRECISION = 4

DATA_DESCRIPTION_CSV = None

REFERENCE_METHOD = None

SIGNIFICANCE_LEVEL = 0.05

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
PBS_MPICOPY = ['{data_dir}', '{exec_dir}', TASK_FILE]
PBS_TIME_REDUCE = 600 # Reduction of runtime in seconds
PBS_LINES_BEFORE = []
PBS_LINES_AFTER = []

""".format(
        task_file=TASKS_FILENAME,
        auto_file=AUTO_FILENAME,
        data_dir=DATASET_DIRNAME,
        exec_dir=EXECS_DIRNAME,
    )
    configfile = os.path.join(os.getcwd(), CONFIG_FILENAME)
    with open(configfile, "w") as fid:
        fid.write(txt)
    mkdir(os.path.join(os.getcwd(), DATASET_DIRNAME))
    mkdir(os.path.join(os.getcwd(), EXECS_DIRNAME))
    touch(AUTO_FILENAME)
    touch(TASKS_FILENAME)
    info("Initialized new Abed project in %s." % os.getcwd())
