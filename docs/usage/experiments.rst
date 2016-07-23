====================
Types of Experiments
====================

Currently, Abed is capable of handling three types of experiments. The type of 
experiment you want to use can be set with the setting :setting:`TYPE`. The 
chosen experiment type has an effect on several settings in the 
:doc:`settings`.

Model assessment
================

:setting:`TYPE` = ``'ASSESS'``.

With this setting, Abed does a grid search on the specified parameters for 
each method, on every specified dataset. It is useful for simple experiments 
with a single dataset per command, or experiments where you want to perform 
cross validation on a dataset. Example settings are::

    TYPE = 'ASSESS'

    DATASETS = ['dataset_1', 'dataset_2']
    METHODS = ['Lasso', 'Ridge']

    costs = [pow(2, x) for x in range(-8, 9, 2)]
    PARAMS = {
        'Lasso': {
            'cost': costs
            },
        'Ridge': {
            'cost': costs
            }
        }

    COMMANDS = {
        'Lasso': ("python {execdir}/lasso.py {datadir}/{dataset}.txt "
            "{cost}"),
        'Ridge': ("python {execdir}/ridge.py {datadir}/{dataset}.txt "
            "{cost}")
        }

where ``lasso.py`` and ``ridge.py`` are python scripts that parse the command 
line arguments, load the dataset specified on the command line, and run `Lasso 
<http://en.wikipedia.org/wiki/Lasso_(statistics)>`_ or `Ridge 
<http://en.wikipedia.org/wiki/Tikhonov_regularization>`_  regression with the 
specified cost parameter, respectively. See also :doc:`executables`.

Note that the executables do not necessarily have to be Python scripts. The 
command will be executed by the system, so it can be an R program executed 
with for instance ``Rscript``, a compiled executable, or anything else.

Also of note is the addition of ``".txt"`` to the ``{dataset}`` variable in 
the command. This implies that we expect the datasets to be stored in files 
``dataset_1.txt`` and ``dataset_2.txt`` in the dataset folder (see 
:setting:`DATADIR`).

Nested Cross-Validation
=======================

:setting:`TYPE` = ``'CV_TT'``

With this setting, a train and test dataset are expected for each command.  
This is useful when you want to train a model on one dataset and test it on 
another, or when you want to run nested cross validation for instance. Example 
settings are as follows::

    TYPE = 'CV_TT'

    DATASETS = [('dataset_1_train', 'dataset_1_test'),
            ('dataset_2_train', 'dataset_2_test')]
    METHODS = ['Lasso', 'Ridge']

    costs = [pow(2, x) for x in range(-8, 9, 2)]
    PARAMS = {
        'Lasso': {
            'cost': costs
            },
        'Ridge': {
            'cost': costs
            }
        }

    COMMANDS = {
        'Lasso': ("python {execdir}/lasso.py {datadir}/{train_dataset}.txt "
            "{datadir}/{test_dataset}.txt {cost}"),
        'Ridge': ("python {execdir}/ridge.py {datadir}/{train_dataset}.txt "
            "{datadir}/{test_dataset}.txt {cost}")
        }

Now it is expected that the executables ``lasso.py`` and ``ridge.py`` accept 
two command line arguments for the datasets. Note that the datasets are 
provided as tuples of training and test datasets.

This option was designed with nested cross validation in mind. One would 
create *K* splits of a dataset on disk, corresponding to separate train and 
test dataset. Then, each executable performs for instance 10-fold cross 
validation on each of the *K* training sets, each time predicting the 
corresponding test dataset.  Results on both the training and test datasets 
would be printed to the output.  Later, the label used for the training data 
can be set using the :setting:`YTRAIN_LABEL` setting. When generating the 
results, Abed will find out which parameter setting performs best on the 
training dataset, and show the performance on the test dataset. See 
:doc:`../api/results/abed.results.cv_tt` for more information.

Raw command file
================

:setting:`TYPE` = ``'RAW'``

This setting can be used for experiments that do not fully fit in either of 
the above frameworks. It allows you to provide a file with commands, through 
the setting :setting:`RAW_CMD_FILE`. The raw command file should contain the 
commands you wish to execute on separate lines (empty lines are allowed). It 
is possible to use the variables ``{execdir}`` and ``{datadir}`` as with the 
other experiment types.  Other variables will not be used however. A command 
file could look like this::


        python {execdir}/lasso.py {datadir}/dataset_1.txt 1.0
        python {execdir}/lasso.py {datadir}/dataset_1.txt 5.0
        python {execdir}/lasso.py {datadir}/dataset_1.txt 10.0
        python {execdir}/lasso.py {datadir}/dataset_1.txt 50.0
        python {execdir}/lasso.py {datadir}/dataset_1.txt 100.0

        python {execdir}/ridge.py {datadir}/dataset_1.txt 1.0
        python {execdir}/ridge.py {datadir}/dataset_1.txt 5.0
        python {execdir}/ridge.py {datadir}/dataset_1.txt 10.0
        python {execdir}/ridge.py {datadir}/dataset_1.txt 50.0
        python {execdir}/ridge.py {datadir}/dataset_1.txt 100.0

Note that now the :setting:`DATASETS` and :setting:`METHODS` settings will not 
be used. The command file should also be added to the git repository, as 
otherwise it will not be uploaded to the cluster.
