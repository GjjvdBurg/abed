#!/usr/bin/env python

"""
Unit tests for the init module of ABED.

"""

import os
import unittest

from abed import init


class AbedInitTestCase(unittest.TestCase):
    def setUp(self):
        self.conf_path = "abed_conf.py"
        self.data_path = "datasets"
        self.exec_path = "execs"
        self.task_path = "abed_tasks.txt"
        self.auto_path = "abed_auto.txt"
        self.expected_config = """
##############################################################################
#                                General Settings                            #
##############################################################################
PROJECT_NAME = ''
TASK_FILE = 'abed_tasks.txt'
AUTO_FILE = 'abed_auto.txt'
RESULT_DIR = '/path/to/local/results'
STAGE_DIR = '/path/to/local/stagedir'
MAX_FILES = 1000
ZIP_DIR = './zips'
LOG_DIR = './logs'
OUTPUT_DIR = './output'
AUTO_SLEEP = 120
HTML_PORT = 8000
COMPRESSION = 'bzip2'

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

##############################################################################
#                               Experiment type                              #
##############################################################################
# Uncomment the desired type
# Model assessment #
#TYPE = 'ASSESS'

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
DATADIR = 'datasets'
EXECDIR = 'execs'

DATASETS = ['dataset_1', 'dataset_2']
DATASET_NAMES = {k:str(i) for i, k in enumerate(DATASETS)}

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
PBS_MPICOPY = ['datasets', 'execs', TASK_FILE]
PBS_TIME_REDUCE = 600 # Reduction of runtime in seconds

"""

    def test_init_config(self):
        """ INIT: Test config is created correctly """
        init.init_config()

        self.assertTrue(os.path.isdir(self.data_path))
        self.assertTrue(os.path.isdir(self.exec_path))
        self.assertTrue(os.path.isfile(self.task_path))
        self.assertTrue(os.path.isfile(self.auto_path))
        self.assertTrue(os.path.isfile(self.conf_path))

        with open(self.conf_path, "r") as fid:
            lines = [l.strip() for l in fid.readlines()]

        exp_lines = [l.strip() for l in self.expected_config.split("\n")]
        counter = 0
        for tl, el in zip(lines, exp_lines):
            print(counter, tl, el)
            self.assertEqual(tl, el)
            counter += 1

    def tearDown(self):
        os.rmdir(self.data_path)
        os.rmdir(self.exec_path)
        os.remove(self.task_path)
        os.remove(self.auto_path)
        os.remove(self.conf_path)


if __name__ == "__main__":
    unittest.main()
