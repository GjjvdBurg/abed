======================
The Abed Settings file
======================

As a user, the settings file is the place where you'll define your experiment 
for Abed. Since there are quite some settings that can be influenced, the 
settings file contains different sections with related settings. These 
sections are reflected in the documentation below.


General settings
================

.. setting:: PROJECT_NAME

``PROJECT_NAME``
----------------

Default: ``''``

.. setting:: TASK_FILE

``TASK_FILE``
-------------

Default: ``'{task_file}'``

.. setting:: AUTO_FILE

``AUTO_FILE``
-------------

Default: ``'{auto_file}'``

.. setting:: RESULT_DIR

``RESULT_DIR``
--------------

Default: ``'/path/to/local/results'``

.. setting:: STAGE_DIR

``STAGE_DIR``
-------------

Default: ``'/path/to/local/stagedir'``

.. setting:: MAX_FILES

``MAX_FILES``
-------------

Default: ``1000``

.. setting:: ZIP_DIR

``ZIP_DIR``
-----------

Default: ``'./zips'``

.. setting:: LOG_DIR

``LOG_DIR``
-----------

Default: ``'./logs'``

.. setting:: OUTPUT_DIR

``OUTPUT_DIR``
--------------

Default: ``'./output'``

.. setting:: AUTO_SLEEP

``AUTO_SLEEP``
--------------

Default: ``120``

.. setting:: HTML_PORT

``HTML_PORT``
--------------

Default: ``8000``

.. setting:: COMPRESSION

``COMPRESSION``
---------------

Default: ``'bzip2'``

Server parameters and settings
==============================

.. setting:: REMOTE_USER

``REMOTE_USER``
---------------

Default: ``'username'``

.. setting:: REMOTE_HOST

``REMOTE_HOST``
---------------

Default: ``'address.of.host'``

.. setting:: REMOTE_DIR

``REMOTE_DIR``
--------------

Default: ``'/home/%s/projects/%s' % (REMOTE_USER, PROJECT_NAME)``

.. setting:: REMOTE_PORT

``REMOTE_PORT``
---------------

Default: ``22``

.. setting:: REMOTE_SCRATCH

``REMOTE_SCRATCH``
------------------

Default: ``None``

.. setting:: REMOTE_SCRATCH_ENV

``REMOTE_SCRATCH_ENV``
----------------------

Default: ``'TMPDIR'``

Settings for Master/Worker program
==================================

.. setting:: MW_SENDATONCE

``MW_SENDATONCE``
-----------------

Default: ``100``

.. setting:: MW_COPY_SLEEP

``MW_COPY_SLEEP``
-----------------

Default: ``120``

Experiment type
===============

.. setting:: TYPE

``TYPE``
--------

Default: ``'ASSESS'``

.. setting:: CV_BASESEED

``CV_BASESEED``
---------------

Default: ``123456``

.. setting:: YTRAIN_LABEL

``YTRAIN_LABEL``
----------------

Default: ``'y_train'``

.. setting:: RAW_CMD_FILE

``RAW_CMD_FILE``
----------------

Default: ``'/path/to/file.txt'``

Build settings
==============

.. setting:: NEEDS_BUILD

``NEEDS_BUILD``
---------------

Default: ``False``

.. setting:: BUILD_DIR

``BUILD_DIR``
-------------

Default: ``'build'``

.. setting:: BUILD_CMD

``BUILD_CMD``
-------------

Default: ``'make all'``

Experiment parameters and settings
==================================

.. setting:: DATADIR

``DATADIR``
-----------

Default: ``'{data_dir}'``

.. setting:: EXECDIR

``EXECDIR``
-----------

Default: ``'{exec_dir}'``

.. setting:: DATASETS

``DATASETS``
------------

Default: ``['dataset_1', 'dataset_2']``

.. setting:: METHODS

``METHODS``
-----------

Default: ``['method_1', 'method_2']``

.. setting:: PARAMS

``PARAMS``
----------

Default::

    {{
        'method_1': {{
            'param_1': [val_1, val_2],
            'param_2': [val_3, val_4],
            'param_3': [val_5, val_6]
            }},
        'method_2': {{
            'param_1': [val_1, val_2, val_3],
            }},
     }}

.. setting:: COMMANDS

``COMMANDS``
------------

Default::

    {{
        'method_1': ("{{execdir}}/method_1 {{datadir}}/{{dataset}} {{param_1}} "
            "{{param_2}} {{param_3}}"),
        'method_2': "{{execdir}}/method_2 {{datadir}}/{{dataset}} {{param_1}}"
    }}

.. setting:: METRICS

``METRICS``
-----------

Default::

    {{
        'NAME_1': {{
            'metric': metric_function_1,
            'best': max
            }},
        'NAME_2': {{
            'metric': metric_function_2,
            'best': min
            }}
    }}

.. setting:: SCALARS

``SCALARS``
-----------

Default::

    {{
        'time': {{
            'best': min
            }},
    }}

.. setting:: RESULT_PRECISION

``RESULT_PRECISION``
--------------------

Default: ``4``

.. setting:: DATA_DESCRIPTION_CSV

``DATA_DESCRIPTION_CSV``
------------------------

Default: ``None``

.. setting:: REFERENCE_METHOD

``REFERENCE_METHOD``
--------------------

Default: ``None``

.. setting:: SIGNIFICANCE_LEVEL

``SIGNIFICANCE_LEVEL``
----------------------

Default: ``0.05``

PBS settings
============

.. setting:: PBS_NODES

``PBS_NODES``
-------------

Default: ``1``

.. setting:: PBS_WALLTIME

``PBS_WALLTIME``
----------------

Default: ``360``

.. setting:: PBS_CPUTYPE

``PBS_CPUTYPE``
---------------

Default: ``None``

.. setting:: PBS_CORETYPE

``PBS_CORETYPE``
----------------

Default: ``None``

.. setting:: PBS_PPN

``PBS_PPN``
-----------

Default: ``None``

.. setting:: PBS_MODULES

``PBS_MODULES``
---------------

Default: ``['mpicopy', 'python/2.7.9']``

.. setting:: PBS_EXPORTS

``PBS_EXPORTS``
---------------

Default: ``['PATH=$PATH:/home/%s/.local/bin/abed' % REMOTE_USER]``

.. setting:: PBS_MPICOPY

``PBS_MPICOPY``
---------------

Default: ``['{data_dir}', EXECDIR, TASK_FILE]``

.. setting:: PBS_TIME_REDUCE

``PBS_TIME_REDUCE``
-------------------

Default: ``600``
