=====================
Overview and Tutorial
=====================

Welcome to the tutorial for Abed!

This document will take you through setting up and running your first 
experiments with Abed. It is assumed that you have already installed Abed both 
locally and on the compute cluster you intend to use, as described in the 
guide on :doc:`installation`.


What is Abed?
=============

Abed was designed to simplify the deployment and analysis of benchmark 
studies in statistics and machine learning, but can also be used as an easy 
way to run tasks on a compute cluster. See :doc:`features` for a complete 
overview of Abed's features.


Using Abed
==========

Note first that Abed is a command line tool, with an interface that should 
familiar to users of **git**. For instance, simply typing::

    $ abed

on the command line, gives an overview of the different commands available in 
Abed. So how do we actually use Abed?


Local setup of an Abed project
------------------------------

First of all, create a new directory for your experiment and switch to it::

    $ mkdir experiment
    $ cd experiment

Next, initialize a new Abed project by typing::

    $ abed init

This does the following:

 - Create a template configuration file ``abed_conf.py``. This is where you 
   will define the settings of your experiments, what methods to run, etc.

 - Create an empty task file ``abed_tasks.txt``. This is where Abed keeps 
   track of which tasks are finished, and which still need to be run. Note 
   that Abed will only store numerical hashes in this file. You shouldn't 
   ever have to edit this file directly.

 - Create an empty auto file ``abed_auto.txt``. This is where Abed keeps 
   track of jobs on the remote compute cluster.

 - Create a directory for datasets ``datasets``. This is where you can place 
   your datasets, but you can also place them somewhere else (see below).

 - Create a directory for executables ``execs``. This is where you'll place 
   the executables that Abed will run.

 - Initialize a git repository, and add the configuration file, task file, and 
   auto file to it, and commit this as the initial commit.

The reason that Abed automatically adds a git repository, is that this makes 
it easy to keep track of changes in the setup of your experiment, add 
executables that you write to version control in the same folder, and keep a 
historical record of your experiments in the interest of reproducible and open 
research. Moreover, the git repository is used to figure out which files to 
commit to the remote server. This means that only files that are in the git 
repository will be transferred to the remote (see below for more info on 
this).

Now that you've initialized the Abed folder, it's time to edit the 
appropriate settings, define tasks, and create executables. Don't forget to 
commit everything to git once you're done. See :doc:`settings` for more 
information on defining the experiments through the settings file.

Remote setup of an Abed project
-------------------------------

Assuming that you've defined everything in the settings file, we should first 
reload the tasks that Abed will run, so the task file corresponds to the 
tasks defined in the settings. This can be done by running::

    $ abed reload_tasks

Once this is done, we can start working with the remote compute cluster. The 
first thing we do is to setup the remote environment, and push the datasets to 
the server. This is done with the command::

    $ abed setup

This creates the following structure on the remote server::

    REMOTE_DIR
    |
    |--- datasets
    |    |
    |    |--- 1464463710
    |    |    |
    |    |    |--- ... your datasets ...
    |    |
    |    packages
    |    |
    |    |--- 2016_05_28_21_30_04_123456ab.tar.gz
    |    |
    |    releases
    |    |
    |    |--- 2016_05_28_21_30_04_123456ab
    |    |    |
    |    |    |--- abed_conf.py
    |    |    |--- abed_auto.txt
    |    |    |--- abed_tasks.txt
    |    |    |--- datasets
    |    |    |--- execs
    |    |         |
    |    |         |--- ... your executables ...
    |    |--- current
    |    |--- previous

In this directory structure, ``current`` and ``previous`` will always be 
symbolic links to the previous two configurations that were uploaded.  
Everytime you use the ``abed push`` command, a new package is uploaded, which 
is unpacked in the release directory. To save space, datasets are copied from 
the previous configuration to the current configuration every time a new push 
is done.

**Note:** *the package that is uploaded is simply an archive made from the 
current state of the git repository. This means that only files that are 
commited to the git repository will be transferred to the remote!*


Running an Abed project
-----------------------

Now that we've finished the setup of Abed both locally and on the remote, 
it's time to start the computations. This can be done by running::

    $ abed push

This pushes the last state of the git repository to the remote server, runs 
the build command (e.g. ``make``) when needed, creates the PBS file, and 
submits this to the PBS queue.

Eventually, the PBS queue will run your job. On the remote server, this is 
also done by Abed. Abed contains an efficient master-worker program 
which works through the Message Passing Interface (MPI). This ensures that 
maximum use is made of all cores on the remote, without the need for any 
additional configurations. Abed will always designate one worker as the 
*copy worker*. This worker process takes care of periodically copying the 
results from the remote scratch directory on the compute node back to your 
project directory. This is useful for when the computations end prematurely, 
this way you will still have most of the results that were generated. Another 
advantage of having the copy worker is that now one core will not be 
continuously occupied, which gives space for potential system processes that 
need to run on the node. Note finally that the master thread does no work 
itself, other than sending out work to the worker threads.

When the computations are finished, the results can be collected using the 
command::

    $ abed pull

This command download the results from the remote server, unpacks them into 
the *staging* directory, and organizes the files into the local *results* 
directory, with a hierarchy based on the datasets and methods in the 
experiment. After the organizing of the results files is done, Abed will 
update the task file to remove all tasks that have been completed, and it will 
automatically commit this to the git repository. Therefore, after this is 
done, it is immediately possible to push again to the remote, to continue the 
computations.

Since it is inefficient manually push and pull every time, the following 
command can be used::

   $ abed auto

This command automatically pushes and pulls, until all tasks are completed.  
For this to work as intended, it must be possible to login to the cluster 
without typing a password. This can be done by exchanging SSH keys, as 
described `here <http://www.rebol.com/docs/ssh-auto-login.html>`_.


When all tasks are finished
---------------------------

When all tasks are finished, Abed automatically generates the summary files 
from the results. If it doesn't do this for whatever reason, you can force 
generation of result pages with the command::

    $ abed parse_results

Both static webpages and simple text files will be generated.  The webpages 
can be viewed simply by running::

    $ abed view_results

This will open the static summary pages in your default browser. For more on 
interpreting and exploring these summary pages, see :doc:`analysis`.
