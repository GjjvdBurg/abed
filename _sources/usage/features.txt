===============
Abed's Features
===============

Abed is a program for managing, performing, and analyzing results of 
(benchmarking) computations on a compute cluster. Typically, such computations 
focus on five main things:

 1. A collection of methods

 2. A set of hyperparameters to optimize for each method

 3. A number of datasets to test the methods on

 4. Various performance metrics on which to evaluate the results

 5. Statistical tests to investigate significant differences between methods.

Abed helps you manage these computations and the subsequent analyses easily, 
and within a single framework.

Features of Abed include:

 - Ability to define a benchmarking experiment through a single comprehensive 
   configuration file.

 - Ability to run external programs for the methods you wish to run, thereby 
   not enforcing methods to be written in a specific language (e.g. methods 
   can be written in R, or as compiled programs, while still using Abed).

 - Ability to execute the computations efficiently on a compute cluster, or 
   locally when desired.

 - When running on a compute cluster, it is possible to set the desired number 
   of compute nodes, computation time, etc. through Abed. This removes the 
   need to learn such specifics.

 - Starting computations on a compute cluster and retrieving the results can 
   be done through two simple Abed commands.

 - Abed has an auto mode, which automatically manages retrieving the results 
   from the compute cluster, evaluating which tasks are left to be done, and 
   submitting a new job to the cluster. This removes the need for long 
   queueing time of large jobs, and means you can have Abed manage your 
   computations while you sleep.

 - Abed generates easy-to-use summary results of the computations as HTML 
   pages and text files.  Both tables and figures are generated which allow 
   you to explore the results, see which methods outperform which other 
   methods.  You can also see whether these statistical differences are 
   significant (see also :doc:`statistical_tests`).

 - Abed manages the entire directory structure on the remote cluster, removing 
   the need to organize this manually.

 - Abed works closely with Git version control software. This makes it easy to 
   keep track of the progress of an experiment, as well as of the software 
   used in the experiment.

 - Since Abed requires storing the full results of experiments, storage space 
   could become an issue. Abed provides a command to compress results, such 
   that this will be less of a problem.
