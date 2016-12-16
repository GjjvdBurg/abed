================================
Defining custom metric functions
================================

It is possible to define custom metric functions for Abed. This can be done by 
defining your metrics in a separate Python file. We will illustrate how to 
define a custom metric function with a practical example. In this example, we 
are interested in the *sparsity hitrate* of an output vector, the proportion 
of correctly identified zeros and correctly identified non-zero elements in 
the vector.

Assume our method outputs the following data::

    beta_true beta_pred
    0.1 0.0
    1.2 1.0
    0 0.1
    0.3 0.2
    0 0.0
    0 0.5
    0.7 0.5

Thus, in 4 out of 7 elements the sparsity is correctly identified (2nd, 4th, 
5th, and 7th element). We can compute this with the following Python code, 
which we place in ``execs/metrics.py``::

    import numpy as np
    from sklearn.metrics import accuracy_score

    def sparsity_hitrate(true, pred):
        """ Compute the sparsity hitrate of a vector. """
        np_true = np.array(true)
        np_pred = np.array(pred)
        return accuracy_score(np_true == 0, np_pred == 0)

To use this metric in Abed's output, we add the following to the Abed settings 
file::

    import imp
    mymetrics = imp.load_source('mymetrics', './execs/metrics.py')

This loads the metrics file as a module in the Abed settings file. Thus, in 
the :setting:`METRICS` setting, we can add::

    METRICS = {
            'HIT': {
                'metric': mymetrics.sparsity_hitrate,
                'best': max
                }
            }

