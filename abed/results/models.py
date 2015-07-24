"""

Models for holding a result cache

"""

import cPickle
import os

from collections import OrderedDict

from abed import settings
from abed.exceptions import AbedHashCollissionException
from abed.utils import dataset_name

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

    def iter_results_dm(self, dataset, method):
        for result in self.cache.itervalues():
            if result.dataset == dataset and result.method == method:
                yield result

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
        self.dataset = dataset_name(dataset)
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

class AbedTableTypes:
    VALUES = 'values'
    RANKS = 'ranks'

class AbedTable(object):
    """

    """

    def __init__(self):
        self.num_columns = 0
        self.num_rows = 0
        self.header = []
        self.rows = None
        self.higher_better = None
        self.type = None
        self.desc = ''
        self.name = ''

    def add_row(self, _id, row):
        if self.rows is None:
            self.rows = OrderedDict()
        if self.rows.has_key(_id):
            raise KeyError('Existing id in table')
        self.rows[_id] = row
        self.num_rows += 1
        if self.num_columns == 0 and len(row) > 0:
            self.num_columns = len(row)

    def table_averages(self):
        averages = [0.0]*self.num_columns
        for _id in self.rows.iterkeys():
            for i, x in enumerate(self.rows[_id]):
                averages[i] += float(x)
        averages = [x/float(self.num_rows) for x in averages]
        return averages

    def table_wins(self):
        hb = self.higher_better
        wins = [0]*self.num_columns
        for _id in self.rows.iterkeys():
            best = float('inf')
            best *= -1 if hb else 1
            best_idx = None
            for i, x in enumerate(self.rows[_id]):
                val = float(x)
                if ((hb and (val > best)) or (not hb and (val < best))):
                    best = x
                    best_idx = i
            if len([x for x in self.rows[_id] if x == best]) == 1:
                wins[best_idx] += 1
        return wins

    def summary_table(self):
        at = AbedTable()
        at.header = self.header[:]
        at.add_row('Average', self.table_averages())
        at.add_row('Wins', self.table_wins())
        return at

    def __iter__(self):
        for _id in self.rows:
            yield (_id, self.rows[_id])
