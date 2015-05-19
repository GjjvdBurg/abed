"""

Models for holding a result cache

"""

import cPickle
import os

from abed import settings
from abed.exceptions import AbedHashCollissionException

class AbedCache(object):
    """

    """

    def __init__(self, methods=None, datasets=None, metrics=None, scalars=None):
        self.methods = set()
        self.datasets = set()
        self.metrics = set()
        self.metric_targets = set()
        self.scalars = set()
        self.cache = {}
        self.cachefile = settings.OUTPUT_DIR + os.sep + 'abed_cache.pkl'

    def dump(self):
        f = open(self.cachefile, 'wb')
        cPickle.dump(self.__dict__, f, 2)
        f.close()

    def load(self):
        if not os.path.exists(self.cachefile):
            raise IOError
        f = open(self.cachefile, 'rb')
        tmp = cPickle.load(f)
        f.close()
        self.__dict__.update(tmp)

    def add_result(self, result):
        if result.hsh in self.cache:
            raise AbedHashCollissionException(result.hsh)
        self.datasets.add(result.dataset)
        self.methods.add(result.method)
        self.metrics = self.metrics.union(result.metrics)
        self.scalars = self.scalars.union(result.scalars)
        self.metric_targets = self.metric_targets.union(result.metric_targets)
        self.cache[result.hsh] = result

    def has_result(self, hsh):
        return (hsh in self.cache)

    def get_metric_values_dm(self, dataset, method, label, metricname):
        for result in self.cache.itervalues():
            if result.dataset == dataset and result.method == method:
                yield result.get_result(label, metric=metricname)

    def get_scalar_values_dm(self, dataset, method, scalarname):
        for result in self.cache.itervalues():
            if result.dataset == dataset and result.method == method:
                yield result.get_result(scalarname)

class AbedResult(object):
    """
    """

    def __init__(self, hsh=None, dataset=None, method=None):
        self.scalars = set()
        self.metrics = set()
        self.metric_targets = set()
        self.results = {}
        self.hsh = hsh
        self.dataset = dataset
        self.method = method

    def add_result_scalar(self, label, value):
        self.scalars.add(label)
        self.results[label] = value

    def add_result_metric(self, label, metric, value):
        self.metrics.add(metric)
        self.metric_targets.add(label)
        if not label in self.results:
            self.results[label] = {}
        self.results[label][metric] = value

    def get_result(self, label, metric=None):
        if metric is None:
            return self.results[label]
        else:
            return self.results[label][metric]

