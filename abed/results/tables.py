"""
General functions for generating tables for Abed results

"""

from .models import AbedTable, AbedTableTypes
from .ranks import make_rank_table
from ..conf import settings


def make_tables_scalar(abed_cache, scalar):
    # First create the normal table
    table = build_tables_scalar(abed_cache, scalar)
    table.higher_better = True if settings.SCALARS[scalar]["best"] == max else False
    table.type = AbedTableTypes.VALUES
    table.desc = "Scalar: %s" % scalar
    table.name = scalar
    table.target = scalar
    table.is_metric = False
    # Now create the rank table from the generated table
    ranktable = make_rank_table(table)
    return [table, ranktable]


def build_tables_scalar(abed_cache, scalarname):
    table = AbedTable()
    table.headers = ["ID"] + sorted(abed_cache.methods)
    for i, dset in enumerate(sorted(abed_cache.datasets)):
        row = []
        for j, method in enumerate(sorted(abed_cache.methods)):
            values = list(abed_cache.get_scalar_values_dm(dset, method, scalarname))
            best_value = settings.SCALARS[scalarname]["best"](values)
            rounded = round(best_value, settings.RESULT_PRECISION)
            fmt = "%%.%df" % settings.RESULT_PRECISION
            row.append(fmt % rounded)
        table.add_row(dset, row)
    return table
