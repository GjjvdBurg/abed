"""
Functions for dealing with result files

We generate several result files for each chosen metric, and some summary files 
with each metric.

TODO:
    time can be measured by OPTIONALLY supplying a line with '% time: <timeval>' 
    in the output file. This must be separated with a ---- line before it.

"""

import os

from abed import settings
from abed.tasks import init_tasks

def iterate_results():
    for subdirs in os.listdir(settings.RESULT_DIR):
        for subdir in subdirs:
            for f in os.listdir(subdir):
                yield f

def hashes_with_method(task_dict, method):
    for hsh in task_dict:
        if task_dict[hsh]['method'] == method:
            yield hsh

def hashes_with_dataset(task_dict, dataset):
    for hsh in task_dict:
        if task_dict[hsh]['dataset'] == dataset:
            yield hsh

def files_with_method(task_dict, method):
    for res_f in iterate_results():
        hsh = int(os.path.splitext(res_f)[0])
        if task_dict[hsh]['method'] == method:
            yield res_f

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

def best_performance_summary(metric):
    # create a table with on the rows the datasets and on the columns the 
    # methods. Each element in the table contains the best performance on the 
    # metric, with the highest value per row containing an asterisk. On the 
    # bottom of the table there is a tally with per column the total number of 
    # 'wins'.
    pass

