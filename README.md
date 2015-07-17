ABED: Automated BEnchmark Distribution in Python
================================================
*Note: ABED is very much a work in process and functionality can break at any 
moment. For a similar and more mature project see: 
[BatchExperiments](https://github.com/tudo-r/BatchExperiments).*

`abed` is an automated system for benchmarking machine learning algorithms. It 
is created for running experiments where it is desired to run multiple methods 
on multiple datasets using multiple parameters. It includes automated 
processing of result files into result tables. `abed` was designed for use 
with the Dutch LISA supercomputer, but can hopefully be used on any Torque 
compute cluster.

`abed` was created as a way to automate all the tedious work necessary to set 
up proper benchmarking experiments. It also removes much of the hassle by 
using a single configuration file for the experimental setup. A core feature 
of `abed` is that it doesn't care about which language the tested methods are 
written in.

Usage:
------

1. Create a skeleton for your project


        abed skeleton


2. Edit configuration, add datasets and executables, and git commit these
3. Create remote directory structure (this will also create task file from 
   config)

        abed setup

4. Push to server

        abed push

5. When tasks are done, collect results

        abed pull

6. Alternatively, automate push/pull using

        abed auto

   This however requires SSH keys to be exchanged with the remote host. See 
for instance, [this](http://www.rebol.com/docs/ssh-auto-login.html) guide.

7. Create summary files using the specified metrics using

        abed parse_results

Dependencies
------------

ABED works only on Python 2 due to the dependency on Fabric. For the list of 
dependencies see `setup.py`.

Installation
------------

To install `abed` only for the current user, run:

    python2 setup.py install --user

Note, if you're on LISA, you need to specify the Python version you wish to 
use by first running:

    module load python/2.7.9

After installation, the executable will be placed in `~/.local/bin`, which you 
should add to your `PATH` variable for convenience, by placing the following 
line in your `~/.bashrc`

    export PATH=$PATH:~/.local/bin/

After this, either open a new terminal or run `source ~/.bashrc`.
	

Requirements
------------

`abed` works with a single configuration file. It was designed for the Dutch 
LISA compute cluster, but can hopefully be generalized to other environments 
as well. Some functionality provided by LISA is used which may not be 
available in other environments:

- Scratch directories: tasks executed through the PBS server are executed on 
  nodes which have a temporary local storage directory, called the "scratch" 
directory. The location of this storage is provided through the TMPDIR 
environment variable, which is used by ABED to place the result files. This 
reduces communication overhead to the users home directory, which is located 
outside the compute node. 

- mpicopy is a command which copies data from the home directory of the user 
  to the scratch directory on the node. The ABED setting 'PBS_MPICOPY' can be 
used to define folders or files which need to be copied to the nodes. In the 
skeleton configuration file the dataset, executable, abed task file are added 
to this list. 

- pbzip2
- mail system, see 
  [here](https://surfsara.nl/systems/lisa/usage/batch-usage#heading18).

Workings
--------

1. Start a new project by running `abed skeleton`
2. Use `abed setup` to setup the remote directory structure.
3. Use `abed push` or `abed auto` to push the data to the remote server, write 
   out the PBS file, and queue it.
4. Use `abed pull` or `abed auto` to pull the results from the remote server, 
   unpack the zip files, update the task list and git commit the updated list.

Running the tasks on the cluster is done as follows:

1. In the PBS the following preprocessing steps are taken:
	a. A `results` directory is created on the scratch filesystem (see 
above)
	b. An email is sent to the current user with a brief summary of the 
number of tasks to be performed. This is sent to the users email, an may 
require a forwarding file to be delivered correctly.
	c. Optional modules are loaded
	d. Optional environment variables are exported
	e. `mpicopy` is used to copy files from the home directory to the 
scratch filesystem
2. `abed run` is executed through `mpiexec`. This requires `abed` to be in the 
   PATH variable. This command is run in a timeout command, with the execution 
time reduced by a configurable number of seconds. This should allow enough 
time for the post-processing steps
3. The postprocessing steps are:
	a. Create a `bzips` directory in the current release directory
	b. Create a compressed archive for each dataset in the result 
directory, this is done in parallel through `pbzip2`
	c. Copy the compressed files to the current release directory
	d. Sent an email to the user that the task is completed.

Notes
-----

1. Installation of ABED and its dependencies must be done under the same 
   Python version. It is recommended to use Python version 2.7.9.

2. ABED currently allows two modes of operation: 'ASSESS' for model 
   assessment, and 'CV_TT' for cross validation with a test dataset. In the 
latter case the datasets need to be specified with '{train_dataset}' and 
'{test_dataset}' in the ABED configuration file.


