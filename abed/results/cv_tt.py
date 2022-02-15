"""

Functions for making result tables specifically for the CV_TT type of
experiments.

In CV_TT experiments, the following is done

1. Labels 'y_train' are expected to exist, with 'y_train_true' and
   'y_train_pred' columns. This must be the true y in the first column, and in 
   the second column the predicted values of y when these indices were in the 
   hold-out fold of cross validation.

2. Labels 'y_test' are expected to exist, with 'y_test_true' and 'y_test_pred'.
   These columns are the true and predicted values of y on the test dataset. 
   Predicted values should (theoretically) be made by training the model on the 
   full training dataset, and predicting the test dataset.

3. Tables are created for each possible metric/metric combination of the metrics
   in the configuration file.  In the tables, each method is given in a single 
   column. In each cell, the performance on the test dataset as measured by the 
   second metric is shown for the parameter configuration for which the 
   performance on the first metric is optimal. This is done for all metric 
   targets other than 'y_train'.

"""

from itertools import product

from .models import AbedTable, AbedTableTypes
from .ranks import make_rank_table
from .tables import make_tables_scalar
from ..conf import settings
from ..io import info
from ..progress import enum_progress


def filter_targets(targets):
    for target in targets:
        if target.startswith(settings.YTRAIN_LABEL):
            continue
        yield target


def cvtt_tables(abed_cache):
    tables = []
    for target in filter_targets(abed_cache.metric_targets):
        for m1, m2 in product(abed_cache.metrics, abed_cache.metrics):
            tables.extend(cvtt_make_tables_metric(abed_cache, m1, m2, target))
    for scalar in abed_cache.scalars:
        tables.extend(make_tables_scalar(abed_cache, scalar))
    return tables


def cvtt_make_tables_metric(abed_cache, train_metric, test_metric, target):
    table = cvtt_build_tables_metric(abed_cache, train_metric, test_metric, target)
    table.higher_better = (
        True if settings.METRICS[test_metric]["best"] == max else False
    )
    table.type = AbedTableTypes.VALUES
    table.desc = "Training metric: %s, testing metric: %s" % (
        train_metric,
        test_metric,
    )
    table.name = "%s_%s" % (train_metric, test_metric)
    table.target = target
    table.is_metric = True
    table.trainmetricname = train_metric
    table.testmetricname = test_metric
    ranktable = make_rank_table(table)
    return [table, ranktable]


def cvtt_build_tables_metric(abed_cache, train_metric, test_metric, target):
    table = AbedTable()
    table.headers = ["ID"] + sorted(abed_cache.methods)
    info(
        "Generating tables for train metric %s, test metric %s, target %s"
        % (train_metric, test_metric, target)
    )
    for i, dset in enum_progress(sorted(abed_cache.datasets), label="Tables"):
        row = []
        for j, method in enumerate(sorted(abed_cache.methods)):
            results = list(abed_cache.iter_results_dm(dset, method))
            values = [
                r.get_result(settings.YTRAIN_LABEL, metric=train_metric)
                for r in results
            ]
            if not values:
                row.append("NaN")
                continue
            best_value = settings.METRICS[train_metric]["best"](values)
            best_results = [
                r
                for r in results
                if r.get_result(settings.YTRAIN_LABEL, metric=train_metric)
                == best_value
            ]
            target_values = [
                r.get_result(target, metric=test_metric) for r in best_results
            ]
            target_best = settings.METRICS[test_metric]["best"](target_values)
            rounded = round(target_best, settings.RESULT_PRECISION)
            fmt = "%%.%df" % settings.RESULT_PRECISION
            row.append(fmt % rounded)
        table.add_row(dset, row)
    return table
