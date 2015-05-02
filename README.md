abed: Automated BEnchmark Distribution
======================================

Usage:

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

7. Create summary files using the specified metrics using

	abed parse_results

Dependencies
------------

ABED depends on the following non-default Python libraries:
	- fabric
	- mpi4py

ABED works only on Python 2 due to the dependency on Fabric.
	

Requirements
------------

`abed` works with a single configuration file. It was designed for the Dutch 
LISA compute cluster, but can hopefully be generalized to other environments 
as well. Some functionality provided by LISA is used which may not be 
available in other environments:

- Scratch directories: tasks executed through the PBS server are executed on 
  nodes which have a temporary local storage directory, called the "scratch" 
directory. The location of this storage is provided through the TMPDIR 
environment variable, which is used by ABED to locate place the result files.  
This reduces communication overhead to the users home directory, which is 
located outside the compute node. 

- mpicopy is a command which copies data from the home directory of the user 
  to the scratch directory on the node. The ABED setting 'PBS_MPICOPY' can be 
used to define folders or files which need to be copied to the nodes. In the 
skeleton configuration file the dataset, executable, abed task file are added 
to this list. 

- timeout
- pbzip2
- mail system

Workings
--------

1. Use 'abed setup' to setup the remote directory structure.
2. Use 'abed push' or 'abed auto' to push the data to the remote server, write 
   out the PBS file, and queue it.
3. Use 'abed pull' or 'abed auto' to pull the results from the remote server, 
   unpack the zip files, update the task list and git commit the updated list.

Running the tasks on the cluster is done as follows:

1. In the PBS the following preprocessing steps are taken:
	a. A 'results' directory is created on the scratch filesystem (see 
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
	a. Create a 'bzips' directory in the current release directory
	b. Create a compressed archive for each dataset in the result 
directory, this is done in parallel through `pbzip2`
	c. Copy the compressed files to the current release directory
	d. Sent an email to the user that the task is completed.

