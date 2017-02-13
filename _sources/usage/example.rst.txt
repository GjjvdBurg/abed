====================================================
Example: Using Abed for comparing regression methods
====================================================

Below we describe a complete walkthrough of an experiment ran using Abed. In 
this example, we will compare three regression methods (OLS, Lasso, and Ridge 
regression) on ten artificial datasets with varying levels of sparsity. Code 
for this experiment can be found on GitHub. There are two versions, `one using 
Python <https://github.com/GjjvdBurg/abed_example_py>`_ for the methods, and 
`one using R <https://github.com/GjjvdBurg/abed_example_R>`_.

Below, the Python version will be described, but differences with the R 
version are minimal.

*Note: throughout this documentation, code lines that start with a $ sign are 
intented to be typed into a terminal.*

Let's begin, first we create a new directory for this experiment, and change 
to it::

   $ mkdir abed_example
   $ cd abed_example

In this directory, we run the following command to initialize Abed::

   $ abed init

This creates the minimal directory structure needed, as well as three files: 
``abed_conf.py``, ``abed_tasks.txt``, and ``abed_auto.txt``. The first file is 
:doc:`settings`, and is the one we will focus on first. 

Defining the experiment
=======================

Let's open the ``abed_conf.py`` file using our favorite editor, and change 
some of the general settings as follows::

   PROJECT_NAME = 'abed_example'
   RESULT_DIR = './results'
   STAGE_DIR = './stagedir'

If you have access to a compute cluster, you can set those parameters in the 
next section of the settings file. If you don't have access to such a server, 
you can skip this section and run the computations locally. For the compute 
cluster, we currently assume it is a PBS type compute cluster, with a scratch 
directory set through an environment variable. The following server parameters 
should definitely be changed::

    REMOTE_USER = 'username'
    REMOTE_HOST = 'address.of.host'

The next section of the settings file defines three variables: 
:setting:`MW_SENDATONCE`, :setting:`MW_COPY_WORKER`, and 
:setting:`MW_COPY_SLEEP`.  In a typical experiment with a sufficient number of 
tasks these settings do not need to be changed from the default. In this case 
however, we will perform a small experiment, so we will set::

    MW_SENDATONCE = 20

Since we don't need intermediate copying of result files, we can set::

    MW_COPY_WORKER = False

Now, on to the next section of the settings file.  This section defines the 
type of experiment we want to run (see :doc:`experiments` for more info).  
Here we'll use the ``'CV_TT'`` type, so we uncomment the following lines::

    TYPE = 'CV_TT'
    CV_BASESEED = 123456
    YTRAIN_LABEL = 'y_train'

The section on "Build settings" can be skipped, as we will implement our 
methods in Python or R for this example. If you want to work with compiled 
executables, you can define the required build procedure here.

The next section of the settings file ("Experiment parameters and settings") 
is arguably the most important, as it defines which tasks will be executed. We 
will leave the :setting:`DATADIR` and :setting:`EXECDIR` unchanged. The 
datasets can be defined as follows::

    DATASETS = [('dataset_%i_train' % i, 'dataset_%i_test' % i) for i in
            range(1, 11)]

This creates a list of pairs with the names of the datasets as pairs of 
training and test datasets: ``['(dataset_1_train', 'dataset_1_test'), 
('dataset_2_train', 'dataset_2_test'), ..., ('dataset_10_train', 
'dataset_10_test')]``. This corresponds to the ``'CV_TT'`` experiment type, as 
described in :doc:`experiments` (please read the documentation there before 
continuing).  Now we can define the methods::

    METHODS = ['OLS', 'Lasso', 'Ridge']

The :setting:`PARAMS` defines the parameters that will be used in the grid 
search, each combination of the parameters will result in a single task, which 
will be executed by Abed. For the Lasso and Ridge methods, only one parameter 
will be varied, the cost parameter. We define this as follows::

    PARAMS = {
            'OLS': {},
            'Lasso': {
                'alpha': [pow(2, x) for x in range(-8, 9, 2)]
                },
            'Ridge': {
                'alpha': [pow(2, x) for x in range(-8, 9, 2)]
                }
            }

This defines the grid of values for the ``alpha`` parameter in Lasso and 
Ridge. Note that OLS needs no parameters. The :setting:`PARAMS` setting 
relates closely to the :setting:`COMMANDS` setting, which we will define now::

    COMMANDS = {
              'OLS': ("python {execdir}/ols.py {datadir}/{train_dataset}.txt "
                  "{datadir}/{test_dataset}.txt"),
              'Lasso': ("python {execdir}/lasso.py "
                  "{datadir}/{train_dataset}.txt {datadir}/{test_dataset}.txt"
                  " {alpha}"),
              'Ridge': ("python {execdir}/ridge.py "
                  "{datadir}/{train_dataset}.txt {datadir}/{test_dataset}.txt"
                  " {alpha}"),
            }

Note that we use ``{alpha}`` in the command for Lasso and Ridge, since we used 
that name in the :setting:`PARAMS` setting above. Below the code for the 
executables will be provided. First, we continue with the next variable in the 
settings file, the :setting:`METRICS` setting. We will use two metrics, the 
mean squared error and the mean absolute error, both provided in the 
scikit-learn package. Since we're using the ``metrics`` submodule from this 
package, we first import it at the top of the settings file, as follows::

    import sklearn.metrics

Then, we define the metrics as::

    METRICS = {
             'MSE': {
                 'metric': sklearn.metrics.mean_squared_error,
                 'best': min,
                 },
             'MAE': {
                 'metric': sklearn.metrics.mean_absolute_error,
                 'best': min,
                 }
             }

Note that we set ``'best'`` for both metrics to ``min``, since lower is 
considered better for both of these metrics. It is also possible to define 
your own metrics, this is described in :doc:`metrics`.

In addition to the metrics defined above, we also want to compare computation 
time of the three methods. For this, we keep the default value of the 
:setting:`SCALARS` setting. The remaining settings in this section will be 
kept on their default values.

The final section of the settings file is the "PBS Settings" section, which 
deals with the PBS server on a compute cluster. Here the desired number of 
nodes and the required computation time can be defined, as well as necessary 
modules and environment variables (see :doc:`settings` for a full 
description). We only change the walltime as follows::

    PBS_WALLTIME = 60


Creating the datasets
=====================

Naturally you will have your own datasets in your simulations. Depending on 
the language you use for your executables, you may or may not have to write 
code for loading the dataset into memory. This is all done in the code you 
write for the methods, to keep Abed lean and allow for language independence.

In this example, we will use ten datasets generated with scikit-learn's 
``make_regression`` function. The full code used for generating the datasets 
can be found in the GitHub repositories (`Python 
<https://github.com/GjjvdBurg/abed_example_py>`_, `R 
<https://github.com/GjjvdBurg/abed_example_R>`_).  The lines that actually 
generate the datasets are::

    X, y, coef = make_regression(n_samples=900, n_features=20,
        n_informative=10, bias=bias, noise=2.0, coef=True,
        random_state=round(random()*1e6))

    X_train, X_test, y_train, y_test = train_test_split(X, y,
        test_size=1.0/3.0, random_state=42)

In this case, datasets are collected as a scikit-learn ``Bunch`` object and 
pickled to a file on disk. All of this is not necessary for Abed, but is just 
the way we're doing it in this example. If you have a different procedure for 
storing and loading datasets, that's no problem in Abed.


Writing the executables
=======================

Abed places no restrictions on the programming language used to implement the 
methods. Here we will use Python to implement the methods. For reference 
however, this example is also available with the methods implemented in R, see 
`this GitHub repository <https://github.com/GjjvdBurg/abed_example_R>`_.

There are not many requirements on the way your executables for your 
experiments are written. However, if you want to make use of the 
:setting:`METRICS` setting, Abed requires you to print the true and the 
predicted values of your target to stdout. Abed will catch this output and 
store it in a text file corresponding to the hash of the task. This is later 
processed by Abed into the output files and result webpages through the 
function :func:`parse_result_fileobj`. If you need to print other information 
to stdout, you can start lines with a '#' symbol, as these lines will be 
skipped. Results written to stdout should start with a label line which tells 
Abed the name of the quantity that is printed. For instance, ``% y_true 
y_pred`` would yield the label ``'y'``. Labels are detected using the 
:func:`find_label` function. Finally, it's also possible to print scalar 
values to the output (computation time for instance). In that case, the name 
of the label should correspond to the name given in the :setting:`SCALARS` 
setting.

Here is an example of output we can expect for this experiment (elipses denote 
continuation and shouldn't be part of the output)::

    # lasso, cost = 1.0
    % y_train_true y_train_pred
    0.352766 0.487470
    0.487392 0.736820
    0.423434 0.470752
    0.379526 0.770139
    0.024067 0.401180
    ...
    % y_test_true y_test_pred
    0.866426 0.979242
    0.487919 0.810133
    0.935068 0.495839
    0.847661 0.396830
    0.092845 0.013258
    ...
    % beta_true beta_pred
    0.221069 0.862545
    0.076156 0.339206
    0.283400 0.998565
    ...
    % time
    0.1329487

When you've finished writing the executables, don't forget to add them to the 
Git repository with ``git add`` and ``git commit``. Remember, only files that 
are part of the git repository or are in the datasets directory will be pushed 
to the compute cluster.

Starting the simulations
========================

When you've finished setting up your experiment, have generated or obtained 
the datasets, and have finished writing the executables, it is then time to 
start the simulations.

First, reload the tasks in Abed to make sure the task file is up to date::

    $ abed reload_tasks

The ``reload_tasks`` command should also be used when you change something in 
:doc:`settings`. After this, it is time to start the simulations. This can be 
done either on a compute cluster, or locally on your computer.

Running on a cluster
------------------------

When you choose to run the simulations on the compute cluster, the first thing 
is to setup the environment for this project on the remote server.  You only 
need to do this once for each experiment::

    $ abed setup

This command sets up the remote directory structure and copies over the 
datasets. It might be useful to take a look at how Abed sets up this remote 
structure. More info on this remote setup can be found in the :doc:`tutorial`.  
Now, it's time to start the simulations with a simple::

    $ abed push

Abed will push the latest version of the Git repository contents to the 
compute cluster, unpack everything there in the ``current`` directory, 
generate a PBS file based on your settings, and submit the job to the queue.  
When all tasks are finished, you can retrieve the compressed results with the 
command::

    $ abed pull

This command downloads the bzipped archives from the ``current`` directory in 
the project folder on the cluster, unpacks them in the staging directory 
(:setting:`STAGE_DIR`), and finally move the results to the 
:setting:`RESULT_DIR`. In this result directory the result files will be 
organized in a hierarchy based on the method and the dataset, for easy lookup.  
The ``pull`` command ends with updating the :setting:`TASK_FILE`, removing the 
hash of tasks that are finished. You can see the remaining tasks with the 
command::

    $ abed status

If more tasks need to be done, you can push again to the compute cluster now.  
The process of pushing and pulling can be automated using the command::

    $ abed auto

For this to be useful however, it is adviced to configure password-less login 
to the compute cluster by exchanging SSH keys.

Running locally
---------------

If you prefer to run the simulations for this example locally, you can do so 
quite easily with Abed. The command you need to run is::

    $ mpiexec abed local

Note that ``mpiexec`` may automatically select the number of cores that are 
used. Please refer to the documentation of the command (``man mpiexec``) for 
more info. Running these computations should not take more than a few minutes.  
The results of these computations will be placed in the :setting:`STAGE_DIR` 
during the computations, and will be organized into the :setting:`RESULT_DIR` 
as a last step. When the computations are finished, the task list needs to be 
updated with the command::

    $ abed update_tasks

If everything went correctly, Abed will show that there are no more tasks to 
be done.

Analyzing the Results
=====================

When Abed detects that all tasks have finished, it will automatically generate 
the summary files from the results. If this fails for some reason, the 
command::

    $ abed parse_results

does the same.

Two types of summary files are generated: text files and HTML pages. The text 
files are simple text tables, whereas the HTML pages include both tables and 
figures. Here, we will focus on the HTML pages. To view the results, type::

    $ abed view_results

This should open your browser and show the main result page of your project.  
At the top of the page you will see links to various tables and figures which 
you can use to explore your results. For a more detailed description of how to 
analyse the results, see :doc:`analysis`.
