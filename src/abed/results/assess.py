
"""
Functions for generating result tables for type 'assess'

"""

from abed import settings
from abed.results.models import AbedTable, AbedTableTypes
from abed.results.ranks import make_rank_table
from abed.results.tables import (make_tables_scalar, write_table)

def assess_tables(abed_cache):
    for target in abed_cache.metric_targets:
        for metric in abed_cache.metrics:
            assess_make_tables_metric(abed_cache, metric, target)
    for scalar in abed_cache.scalars:
        make_tables_scalar(abed_cache, scalar)

def assess_make_tables_metric(abed_cache, metric, target):
    # First create the normal table
    table = assess_build_tables_metric(abed_cache, metric, target)
    table.higher_better = (True if settings.METRICS[metric]['best'] == max else 
            False)
    table.type = AbedTableTypes.VALUES
    table.desc = 'Metric: %s' % metric
    table.name = metric
    table.target = target
    table.is_metric = True
    write_table(table, output_formats=settings.OUTPUT_FORMATS)
    # Now create the rank table from the generated table
    ranktable = make_rank_table(table)
    write_table(ranktable, output_formats=settings.OUTPUT_FORMATS)

def assess_build_tables_metric(abed_cache, metricname, metric_label):
    table = AbedTable()
    table.headers = ['ID'] + sorted(abed_cache.methods)
    for i, dset in enumerate(sorted(abed_cache.datasets)):
        row = []
        for j, method in enumerate(sorted(abed_cache.methods)):
            values = list(abed_cache.get_metric_values_dm(dset, method, 
                metric_label, metricname))
            best_value = settings.METRICS[metricname]['best'](values)
            rounded = round(best_value, settings.RESULT_PRECISION)
            fmt = '%%.%df' % settings.RESULT_PRECISION
            row.append(fmt % rounded)
        table.add_row(dset, row)
    return table
