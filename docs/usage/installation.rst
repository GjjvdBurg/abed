=============================
Installation and Requirements
=============================

Basic Installation
------------------

To install Abed only for the current user, run::

    $ python2 setup.py install --user

Note, if you're on LISA, you need to specify the Python version you wish to 
use by first running::

    $ module load python/2.7.9

After installation, the executable will be placed in ``~/.local/bin``, which you 
should add to your ``PATH`` variable for convenience, by placing the following 
line in your ``~/.bashrc``::

    export PATH=$PATH:~/.local/bin/

After this, either open a new terminal or run ``source ~/.bashrc``.

**Note:** *Installation of Abed and its dependencies must be done under the 
same Python version.*

Requirements
------------

Abed works with a single configuration file. It was designed for the Dutch 
LISA compute cluster, but can hopefully be generalized to other environments 
as well. Some functionality provided by LISA is used which may not be 
available in other environments:

- Scratch directories: tasks executed through the PBS server are executed on 
  nodes which have a temporary local storage directory, called the "scratch" 
  directory. The location of this storage is provided through the TMPDIR 
  environment variable, which is used by Abed to place the result files. This 
  reduces communication overhead to the users home directory, which is located 
  outside the compute node.
- mpicopy is a command which copies data from the home directory of the user 
  to the scratch directory on the node. The Abed setting 'PBS_MPICOPY' can be 
  used to define folders or files which need to be copied to the nodes. In the 
  skeleton configuration file the dataset, executable, abed task file are 
  added to this list.
- pbzip2
- mail system, see `here 
  <https://surfsara.nl/systems/lisa/usage/batch-usage#heading18>`_


