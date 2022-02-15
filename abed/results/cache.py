"""
Functions for creating the result cache.

The result cache is basically a dictionary between the hashes and the metrics
that we want to know for each hash.
"""

from .models import AbedCache, AbedResult
from .walk import walk_for_cache
from ..conf import settings
from ..io import info, warning


def find_label(line):
    for scalar in settings.SCALARS:
        if scalar in line:
            return scalar
    return "_".join(line.split(" ")[1].split("_")[:-1])


def parse_result_fileobj(fid, hsh, dataset, method):
    data = {}
    label = None
    for line in fid:
        l = line.strip()
        # Skip comment lines
        if l.startswith("#"):
            continue
        elif l.startswith("%"):
            label = find_label(l)
            if label in settings.SCALARS:
                data[label] = None
            else:
                data[label] = {"true": [], "pred": []}
            continue
        if label in settings.SCALARS:
            # If we already have data for a label, we continue to avoid
            # overwriting it
            if data[label]:
                continue
            try:
                data[label] = float(l)
            except ValueError:
                warning(
                    "Could not parse scalar metric '%s' for "
                    "file with hash %s. Skipping.\nOffending line: %s" % (label, hsh, l)
                )
                continue
        else:
            try:
                if "\t" in l:
                    true, pred = l.split("\t")
                else:
                    true, pred = l.split(" ")
                data[label]["true"].append(float(true))
                data[label]["pred"].append(float(pred))
            except ValueError:
                warning(
                    "Could not parse true/pred metric '%s' for "
                    "file %s. Skipping.\nOffending line: %s" % (label, hsh, l)
                )
                continue
    fid.close()

    ar = AbedResult(hsh, dataset=dataset, method=method)

    for label in data.keys():
        if label in settings.SCALARS:
            ar.add_result_scalar(label, data[label])
        else:
            for metric in settings.METRICS:
                metric_func = settings.METRICS[metric]["metric"]
                ar.add_result_metric(
                    label,
                    metric,
                    metric_func(data[label]["true"], data[label]["pred"]),
                )
    return ar


def init_result_cache(task_dict):
    ac = AbedCache(
        methods=settings.METHODS,
        datasets=settings.DATASETS,
        metrics=settings.METRICS,
        scalars=settings.SCALARS,
    )
    counter = 0
    for dataset, method, fid, hsh in walk_for_cache(ac):
        result = parse_result_fileobj(fid, hsh, dataset, method)
        if result is None:
            continue
        ac.add_result(result)
        counter += 1
    ac.dump()
    info("Read %i result files into cache." % counter)
    return ac


def update_result_cache(task_dict, skip_cache=False):
    ac = AbedCache()
    try:
        ac.load()
        info("Result cache loaded from disk.")
    except IOError:
        info("Result cache non-existent, generating it.")
        ac = init_result_cache(task_dict)
        return ac

    # User requested skip of cache regeneration
    if skip_cache:
        warning("Skipping cache regeneration check on user request.")
        return ac

    # updating the result cache is done in two steps:
    # 1. Check if new metrics or scalars are added, if so regenerate everything
    # 2. Check if new result files are added, if that's the case only generate
    # those
    conf_metrics = set(settings.METRICS.keys())
    cache_metrics = ac.metrics
    diff = conf_metrics - cache_metrics
    if len(diff) > 0:
        ac = init_result_cache(task_dict)
        return ac

    for dataset, method, fid, hsh in walk_for_cache(ac):
        result = parse_result_fileobj(fid, hsh, dataset, method)
        if result is None:
            continue
        ac.add_result(result)

    ac.dump()
    return ac
