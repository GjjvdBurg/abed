==============
How Abed works
==============

Running the tasks on the cluster is done as follows:

1. In the PBS the following preprocessing steps are taken:

        a. A ``results`` directory is created on the scratch filesystem (see
           above)

        b. An email is sent to the current user with a brief summary of the
           number of tasks to be performed. This is sent to the users email, 
           an may require a forwarding file to be delivered correctly.

	c. Optional modules are loaded

	d. Optional environment variables are exported

        e. ``mpicopy`` is used to copy files from the home directory to the
           scratch filesystem

2. ``abed run`` is executed through ``mpiexec``. This requires Abed to be in the 
   PATH variable. This command is run in a timeout command, with the execution 
   time reduced by a configurable number of seconds. This should allow enough 
   time for the post-processing steps

3. The postprocessing steps are:

	a. Create a ``bzips`` directory in the current release directory
        b. Create a compressed archive for each dataset in the result
           directory, this is done in parallel through ``pbzip2``
	c. Copy the compressed files to the current release directory
	d. Sent an email to the user that the task is completed.


