"""
Functions for creating the result cache.

The result cache is basically a dictionary between the hashes and the metrics 
that we want to know for each hash.
"""

import marshal
import os

from abed import settings
from abed.results.walk import walk_results
from abed.utils import info, hash_from_filename

def find_label(line):
    for scalar in settings.SCALARS:
        if scalar in line:
            return scalar
    return line.split(' ')[1].split('_')[0]

def parse_result_file(filepath):
    data = {}
    fid = open(filepath, 'r')
    label = None
    for line in fid:
        l = line.strip()
        if l.startswith('%'):
            label = find_label(l)
            if label in settings.SCALARS:
                data[label] = None
            else:
                data[label] = {'true': [], 'pred': []}
            continue
        if label in settings.SCALARS:
            data[label] = float(l)
        else:
            true, pred = l.split('\t')
            data[label]['true'].append(float(true))
            data[label]['pred'].append(float(pred))
    fid.close()

    output = {'SCALARS': {}, 'METRICS': {}}
    for label in data.iterkeys():
        if label in settings.SCALARS:
            output['SCALARS'][label] = data[label]
        else:
            for metric in settings.METRICS:
                metric_func = settings.METRICS[metric]['metric']
                output['METRICS'][metric] = metric_func(data[label]['true'], 
                        data[label]['pred'])
    return output

def create_result_cache(task_dict):
    cache = {}
    info("Starting cache generation")
    for dataset, method, files in walk_results():
        info("Dataset: %s\tmethod = %s" % (dataset, method))
        for f in files:
            hsh = hash_from_filename(f)
            cache[hsh] = parse_result_file(f)
    cachefile = settings.OUTPUT_DIR + os.sep + 'abed_cache.msh'
    with open(cachefile, 'wb') as cid:
        info("Starting dump to %s" % cachefile)
        marshal.dump(cache, cid)
        info("Dump finished.")



def update_result_cache():
    pass

