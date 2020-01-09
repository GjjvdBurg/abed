================
Welcome to Abed!
================

`abed <https://github.com/GjjvdBurg/abed>`_ is an automated system for 
benchmarking machine learning algorithms.  It is created for running 
experiments where it is desired to run multiple methods on multiple datasets 
using multiple parameters. It includes automated processing of result files 
into result tables and figures. 

``abed`` is available on PyPI::

    $ pip install abed

``abed`` was created as a way to automate all the tedious work necessary to 
set up proper benchmarking experiments. It also removes much of the hassle by 
using a single configuration file for the experimental setup. A core feature 
of ``abed`` is that it doesn't care about which language the tested methods are 
written in.

``abed`` can create output tables as either simple txt files, or as html pages 
using the excellent `DataTables <https://datatables.net/>`_ plugin. To support 
offline operation the necessary DataTables files are packaged with ``abed``.

Documentation
-------------

For ``abed``'s documentation, see `the documentation 
<https://gjjvdburg.github.io/abed/docs.html>`_.

Screenshots
-----------

|figure1|_ |figure2|_ |figure3|_

.. _figure1: https://raw.githubusercontent.com/GjjvdBurg/abed/master/.github/rank_plots.png
.. _figure2: https://raw.githubusercontent.com/GjjvdBurg/abed/master/.github/tables.png
.. _figure3: https://raw.githubusercontent.com/GjjvdBurg/abed/master/.github/tables_time.png

.. |figure1| image:: https://raw.githubusercontent.com/GjjvdBurg/abed/master/.github/rank_plots.png
        :alt: Rank plots in Abed
        :width: 32%
        :align: middle

.. |figure2| image:: https://raw.githubusercontent.com/GjjvdBurg/abed/master/.github/tables.png
        :alt: Result tables in Abed
	:width: 32%
	:align: middle

.. |figure3| image:: https://raw.githubusercontent.com/GjjvdBurg/abed/master/.github/tables_time.png
        :alt: Result tables in Abed (time)
	:width: 32%
	:align: middle


Notes
-----

The current version of ``abed`` is very usable. However, it is still considered 
beta software, as it is not yet completely documented and some robustness 
improvements are planned. For a similar and more mature project which works 
with R see: `BatchExperiments <https://github.com/tudo-r/BatchExperiments>`_.
