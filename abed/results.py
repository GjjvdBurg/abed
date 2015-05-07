"""
Functions for dealing with result files

We generate several result files for each chosen metric, and some summary files 
with each metric.

The following directory structure is assumed:

    settings.RESULT_DIR / {dataset} / {method} / [files]

"""

import datetime
import os
import numpy as np

from matplotlib import mlab, pyplot
from tabulate import tabulate

from abed import settings
from abed.exceptions import (AbedNonstandardMetricDirection, 
        AbedDatasetdirNotFoundException, AbedMethoddirNotFoundException)
from abed.progress import enum_progress
from abed.tasks import init_tasks
from abed.utils import info

basename = os.path.basename
splitext = os.path.splitext

def hashes_with_method(task_dict, method):
    for hsh in task_dict:
        if task_dict[hsh]['method'] == method:
            yield hsh

def hashes_with_dataset(task_dict, dataset):
    for hsh in task_dict:
        if task_dict[hsh]['dataset'] == dataset:
            yield hsh

def files_w_method(task_dict, method):
    for dset in os.listdir(settings.RESULT_DIR):
        dpath = '%s%s%s' % (settings.RESULT_DIR, os.sep, dset)
        methdirs = os.listdir(dpath)
        if not method in methdirs:
            raise AbedMethoddirNotFoundException
        mpath = '%s%s%s' % (dpath, os.sep, method)
        for f in os.listdir(mpath):
            fname = '%s%s%s' % (mpath, os.sep, f)
            yield fname

def files_w_dataset(task_dict, dataset):
    dset = splitext(basename(dataset))[0]
    if dset not in os.listdir(settings.RESULT_DIR):
        raise AbedDatasetdirNotFoundException
    dpath = '%s%s%s' % (settings.RESULT_DIR, os.sep, dset)
    for method in os.listdir(dpath):
        mpath = '%s%s%s' % (dpath, os.sep, method)
        for f in os.listdir(mpath):
            fname = '%s%s%s' % (mpath, os.sep, f)
            yield fname

def files_w_dset_and_method(task_dict, dataset, method):
    dset = splitext(basename(dataset))[0]
    if dset not in os.listdir(settings.RESULT_DIR):
        raise AbedDatasetdirNotFoundException(dset)
    dpath = '%s%s%s' % (settings.RESULT_DIR, os.sep, dset)
    methdirs = os.listdir(dpath)
    if not method in methdirs:
         raise AbedMethoddirNotFoundException(method)
    mpath = '%s%s%s' % (dpath, os.sep, method)
    for f in os.listdir(mpath):
        fname = '%s%s%s' % (mpath, os.sep, f)
        yield fname

def mean_over_datasets(metric):
    # per parameter configuration average metric value on all dataset
    pass

def mean_over_params(metric):
    # per dataset average metric value over all parameters
    pass

def best_over_datasets(metric, higher_better=True):
    # best parameter configuration on metric among all datasets
    pass

def best_over_params(metric, higher_better=True):
    # best dataset on metric over all parameters
    pass

def generate_per_method():
    for metric in settings.METRICS:
        for method in settings.METHODS:
            mean_over_datasets(metric, method)
            mean_over_params(metric, method)
            best_over_datasets(metric, method)
            best_over_params(metric, method)

def find_label(line):
    if line.startswith('% time'):
        return 'time'
    else:
        return line.split(' ')[1].split('_')[0]

def parse_result_file(f, metric):
    data = {}
    fid = open(f, 'r')
    label = None
    for line in fid:
        l = line.strip()
        if l.startswith('%'):
            label = find_label(l)
            if label == 'time':
                data[label] = None
            else:
                data[label] = {'true': [], 'pred': []}
            continue
        if label == 'time':
            data[label] = float(l)
        else:
            true, pred = l.split('\t')
            data[label]['true'].append(float(true))
            data[label]['pred'].append(float(pred))

    out = {}
    for label in data.iterkeys():
        if label == 'time':
            out[label] = data[label]
        else:
            out[label] = metric(data[label]['true'], data[label]['pred'])
    return out

def performance_density(metric, metricname):
    # create density plots of the performance of each method on the metric

    # TODO:
    # - write out to file
    # - make a lot nicer
    # - smooth density plots

    all_tasks = init_tasks()

    num_datasets = len(settings.DATASETS)
    num_methods = len(settings.METHODS)

    m_func = metric['metric']
    b_func = metric['best']

    meth_perf = {key:{} for key in settings.METHODS}

    for i, dset in enum_progress(sorted(settings.DATASETS), label='Datasets: '):
        for j, method in enumerate(sorted(settings.METHODS)):
            for res_file in files_w_dset_and_method(all_tasks, dset, method):
                out_dict = parse_result_file(res_file, m_func)
                for key in out_dict:
                    if not key in meth_perf[method]:
                        meth_perf[method][key] = []
                    meth_perf[method][key].append(out_dict[key])

    num_bins = 25
    for method in sorted(settings.METHODS):
        for key in meth_perf[method]:
            n, bins, patches = pyplot.hist(meth_perf[method][key], num_bins, 
                    normed=1)
            pyplot.show()


def best_performance_summary(metric, metricname):
    # create a table with on the rows the datasets and on the columns the 
    # methods. Each element in the table contains the best performance on the 
    # metric, with the highest value per row containing an asterisk. On the 
    # bottom of the table there is a tally with per column the total number of 
    # 'wins'.
    all_tasks = init_tasks()
    tables = {}

    num_datasets = len(settings.DATASETS)
    num_methods = len(settings.METHODS)

    m_func = metric['metric']
    b_func = metric['best']

    for i, dset in enum_progress(sorted(settings.DATASETS), label='Datasets: '):
        for j, method in enumerate(sorted(settings.METHODS)):
            values = []
            for res_file in files_w_dset_and_method(all_tasks, dset, method):
                values.append(parse_result_file(res_file, m_func))

            try:
                keys = values[0].keys()
            except IndexError:
                import code
                code.interact(local=dict(globals(), **locals()))
            if not tables:
                for key in keys:
                    tables[key] = np.zeros((num_datasets, num_methods))

            for key in keys:
                if key == 'time':
                    tables[key][i, j] = min([x[key] for x in values])
                else:
                    tables[key][i, j] = b_func([x[key] for x in values])

    for key in keys:
        table = []
        wincount = [0]*len(settings.METHODS)
        dsetlength = -1
        if key == 'time':
            bestidxs = tables[key].argmin(1)
        else:
            if b_func == min:
                bestidxs = tables[key].argmin(1)
            elif b_func == max:
                bestidxs = tables[key].argmax(1)
            else:
                raise AbedNonstandardMetricDirection

        for i, dset in enumerate(sorted(settings.DATASETS)):
            dsetlength = max(dsetlength, len(dset))
            row = [splitext(basename(dset))[0]]
            for j, method in enumerate(sorted(settings.METHODS)):
                if j == bestidxs[i]:
                    row.append('%4.4f*' % tables[key][i, j])
                    wincount[j] += 1
                else:
                    row.append('%4.4f' % tables[key][i, j])
            table.append(row)
        dashrow = ['-'*dsetlength] + ['-'*len(x) for x in 
                sorted(settings.METHODS)]
        table.append(dashrow)
        table.append(['Total best'] + [str(x) for x in wincount])

        opath = '{respath}/ABED_{metric}_{key}.txt'.format(
                respath=settings.OUTPUT_DIR, metric=metricname, key=key)
        now = datetime.datetime.now()
        headers = [''] + sorted(settings.METHODS)
        with open(opath, 'w') as oid:
            oid.write("%% Result file generated by ABED at %s\n" % 
                    now.strftime('%c'))
            oid.write("%% Table for key: %s\n" % key)
            oid.write("%% Metric: %s\n\n" % metricname)
            oid.write(tabulate(table, headers=headers))
        info("Created output file: %s" % opath)


def make_results():
    for metric in settings.METRICS.iterkeys():
        info("Getting performance density plots for metric %s" % metric)
        performance_density(settings.METRICS[metric], metric)
        info("Getting performance summary with metric %s" % metric)
        best_performance_summary(settings.METRICS[metric], metric)

