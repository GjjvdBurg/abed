"""
Functions for evaluating statistically significant differences between 
methods.
"""

from scipy.stats import f as f_dist
from scipy.stats import norm as norm_dist
from math import sqrt

from .models import AbedTableTypes
from ..conf import settings
from ..io import error


def global_difference(table):
    """ Runs and F-test on the ranks. """
    if (not table.is_summary) or (table.type != AbedTableTypes.RANKS):
        return None
    N = float(len(settings.DATASETS))
    k = float(len(settings.METHODS))
    averages = next((row for _id, row in table if _id == "Average"), None)
    av_sq = sum([pow(float(x), 2.0) for x in averages])
    chi2 = 12.0 * N / (k * (k + 1)) * (av_sq - (k * pow(k + 1, 2.0) / 4.0))

    # this can happen when the ordering of methods is always the same
    try:
        Fstat = (N - 1.0) * chi2 / (N * (k - 1) - chi2)
    except ZeroDivisionError:
        Fstat = float("inf")
    Fprob = 1.0 - f_dist.cdf(Fstat, k - 1, (k - 1) * (N - 1))
    return Fstat, Fprob


def reference_difference(table):
    """ Runs Holm's procedure for a reference classifier. """
    # Sanity checks
    if settings.REFERENCE_METHOD is None:
        return None
    if (not table.is_summary) or (table.type != AbedTableTypes.RANKS):
        return None
    if not settings.REFERENCE_METHOD in settings.METHODS:
        error("Reference method %s not in list of methods." % settings.REFERENCE_METHOD)
        raise SystemExit

    # define constants
    N = float(len(settings.DATASETS))
    k = float(len(settings.METHODS))
    av_ranks = next((row for _id, row in table if _id == "Average"), None)
    av_ranks = [float(x) for x in av_ranks]
    ref_idx = settings.METHODS.index(settings.REFERENCE_METHOD)
    others = [m for m in settings.METHODS if not m == settings.REFERENCE_METHOD]

    # Calculate the Z-scores compared to the reference method
    Z_scores = [0] * len(others)
    P_values = [0] * len(others)
    constant = sqrt((6.0 * N) / (k * (k + 1.0)))
    for j, method in enumerate(others):
        i = settings.METHODS.index(method)
        Z_scores[j] = (av_ranks[ref_idx] - av_ranks[i]) * constant
        P_values[j] = norm_dist.cdf(Z_scores[j])

    # Sort the p-values in ascending order
    sorted_pvals = sorted((p, i) for i, p in enumerate(P_values))

    # Calculate significant differences following Holm's procedure
    significant_differences = [False] * len(others)
    CD_threshold = None
    for i in range(int(k - 1)):
        threshold = settings.SIGNIFICANCE_LEVEL / float(k - (i + 1))
        pval, idx = sorted_pvals[i]
        significant_differences[idx] = pval < threshold
        if pval > threshold and CD_threshold is None:
            CD_threshold = threshold

    CD = -1 * norm_dist.ppf(CD_threshold) / constant
    out = list(zip(others, Z_scores, P_values, significant_differences))
    return out, CD
