"""
Functions for generating fractional ranks

"""

from .models import AbedTable, AbedTableTypes
from ..conf import settings


def get_ranks(x):
    """
    Get ranks for a vector. This function assumes lower is better, so high
    numbers get a high rank. You can invert it with: [len(x) - t + 1 for t
    in ranks]

    >>> x = [7, 0.1, 0.5, 0.1, 10, 100, 200]
    >>> get_ranks(x)
    [4.0, 1.5, 3.0, 1.5, 5.0, 6.0, 7.0]
    """
    l = len(x)
    r = 1
    ranks = [0] * l
    while not all([k is None for k in x]):
        m = min([k for k in x if not k is None])
        idx = [1 if k == m else 0 for k in x]
        s = sum(idx)
        ranks = [r + (s - 1) / 2.0 if idx[k] else ranks[k] for k in range(l)]
        r += s
        x = [None if idx[k] else x[k] for k in range(l)]
    return ranks


def make_rank_table(table):
    ranktable = AbedTable()
    ranktable.headers = table.headers[:]
    ranktable.higher_better = False
    ranktable.type = AbedTableTypes.RANKS
    ranktable.desc = table.desc
    ranktable.name = table.name
    ranktable.target = table.target
    ranktable.is_metric = table.is_metric
    if settings.TYPE == "ASSESS":
        ranktable.metricname = table.metricname
    elif settings.TYPE == "CV_TT":
        ranktable.trainmetricname = table.trainmetricname
        ranktable.testmetricname = table.testmetricname

    for _id, row in table:
        ranks = get_ranks(row)
        if table.higher_better:
            ranks = [len(ranks) - t + 1 for t in ranks]
        ranktable.add_row(_id, ranks)
    return ranktable
