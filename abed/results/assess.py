"""
Functions for generating result tables for type 'assess'

"""

from .models import AbedTable, AbedTableTypes
from .ranks import make_rank_table
from .tables import make_tables_scalar
from ..conf import settings


def assess_tables(abed_cache):
    tables = []
    for target in abed_cache.metric_targets:
        for metric in abed_cache.metrics:
            tables.extend(assess_make_tables_metric(abed_cache, metric, target))
    for scalar in abed_cache.scalars:
        tables.extend(make_tables_scalar(abed_cache, scalar))
    return tables


def assess_make_tables_metric(abed_cache, metric, target):
    # First create the normal table
    table = assess_build_tables_metric(abed_cache, metric, target)
    table.higher_better = True if settings.METRICS[metric]["best"] == max else False
    table.type = AbedTableTypes.VALUES
    table.desc = "Metric: %s" % metric
    table.name = metric
    table.target = target
    table.is_metric = True
    table.metricname = metric
    # Now create the rank table from the generated table
    ranktable = make_rank_table(table)
    return [table, ranktable]


def assess_build_tables_metric(abed_cache, metricname, metric_label):
    table = AbedTable()
    table.headers = ["ID"] + sorted(abed_cache.methods)
    for i, dset in enumerate(sorted(abed_cache.datasets)):
        row = []
        for j, method in enumerate(sorted(abed_cache.methods)):
            values = list(
                abed_cache.get_metric_values_dm(dset, method, metric_label, metricname)
            )
            best_value = settings.METRICS[metricname]["best"](values)
            rounded = round(best_value, settings.RESULT_PRECISION)
            fmt = "%%.%df" % settings.RESULT_PRECISION
            row.append(fmt % rounded)
        table.add_row(dset, row)
    return table
