"""

Models for holding a result cache

"""

import os

from collections import OrderedDict
from six.moves import cPickle

from ..conf import settings
from ..datasets import dataset_name
from ..exceptions import AbedHashCollissionException
from ..utils import mkdir


class AbedCache(object):
    """"""

    def __init__(
        self,
        methods=None,
        datasets=None,
        metrics=None,
        scalars=None,
        cachefile=None,
    ):
        self.methods = set()
        self.datasets = set()
        self.metrics = set()
        self.metric_targets = set()
        self.scalars = set()
        self.cache = {}
        if cachefile is None:
            self.cachefile = settings.OUTPUT_DIR + os.sep + "abed_cache.pkl"
        else:
            self.cachefile = cachefile

    def dump(self):
        mkdir(os.path.dirname(self.cachefile))
        f = open(self.cachefile, "wb")
        cPickle.dump(self.__dict__, f, 2)
        f.close()

    def load(self):
        if not os.path.exists(self.cachefile):
            raise IOError
        f = open(self.cachefile, "rb")
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
        return hsh in self.cache

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

    def __repr__(self):
        return "AbedCache(n_results=%i)" % len(self.cache)

    def __str__(self):
        return repr(self)

    def __iter__(self):
        for hsh in self.cache:
            yield self.cache[hsh]


class AbedResult(object):
    """"""

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

    def __str__(self):
        s = "AbedResult(hsh=%r, dataset=%r, method=%r, results=%r)" % (
            self.hsh,
            self.dataset,
            self.method,
            self.results,
        )
        return s

    def __repr__(self):
        return str(self)


class AbedTableTypes:
    VALUES = "values"
    RANKS = "ranks"


class AbedTable(object):
    """"""

    def __init__(self):
        self.num_columns = 0
        self.num_rows = 0
        self.headers = None
        self.rows = None
        self.higher_better = None
        self.type = None
        self.desc = ""
        self.name = ""
        self.target = None
        self.is_metric = True
        self.is_summary = False
        if settings.TYPE == "ASSESS":
            self.metricname = None
        elif settings.TYPE == "CV_TT":
            self.trainmetricname = None
            self.testmetricname = None

    def add_row(self, _id, row):
        if self.rows is None:
            self.rows = OrderedDict()
        if self.rows.has_key(_id):
            raise KeyError("Existing id in table")
        self.rows[_id] = row
        self.num_rows += 1
        if self.num_columns == 0 and len(row) > 0:
            self.num_columns = len(row)

    def table_averages(self):
        averages = [0.0] * self.num_columns
        for _id in self.rows.keys():
            for i, x in enumerate(self.rows[_id]):
                averages[i] += float(x)
        averages = [x / float(self.num_rows) for x in averages]
        fmtavg = []
        for num in averages:
            rounded = round(num, settings.RESULT_PRECISION)
            fmt = "%%.%df" % settings.RESULT_PRECISION
            fmtavg.append(fmt % rounded)
        return fmtavg

    def table_wins(self):
        hb = self.higher_better
        wins = [0] * self.num_columns
        for _id in self.rows.keys():
            best = float("inf")
            best *= -1 if hb else 1
            best_idx = None
            for i, x in enumerate(self.rows[_id]):
                val = float(x)
                if (hb and (val > best)) or ((not hb) and (val < best)):
                    best = val
                    best_idx = i
            if len([x for x in self.rows[_id] if float(x) == best]) == 1:
                wins[best_idx] += 1
        return wins

    def table_losses(self):
        hb = self.higher_better
        losses = [0] * self.num_columns
        for _id in self.rows.keys():
            worst = float("inf")
            worst *= 1 if hb else -1
            worst_idx = None
            for i, x in enumerate(self.rows[_id]):
                val = float(x)
                if (hb and (val < worst)) or ((not hb) and (val > worst)):
                    worst = val
                    worst_idx = i
            if len([x for x in self.rows[_id] if float(x) == worst]) == 1:
                losses[worst_idx] += 1
        return losses

    def table_ties(self):
        num_ties = 0
        for _id in self.rows.keys():
            values = [float(x) for x in self.rows[_id]]
            num_uniq = len(set(values))
            if num_uniq == 1:
                num_ties += 1
        ties = [num_ties] * self.num_columns
        return ties

    def summary_table(self):
        at = AbedTable()
        at.headers = self.headers[:]
        at.type = self.type
        at.desc = self.desc
        at.name = self.name
        at.target = self.target
        at.is_metric = self.is_metric
        if settings.TYPE == "ASSESS":
            at.metricname = self.metricname
        elif settings.TYPE == "CV_TT":
            at.trainmetricname = self.trainmetricname
            at.testmetricname = self.testmetricname
        at.add_row("Average", self.table_averages())
        at.add_row("Wins", self.table_wins())
        at.add_row("Losses", self.table_losses())
        at.add_row("Ties", self.table_ties())
        at.is_summary = True
        return at

    def left_insert(self, other):
        summary = self.summary_table()
        self.num_columns += other.num_columns
        self.headers = other.headers + self.headers[1:]
        for _id, otherrow in other:
            myrow = self.rows.get(_id, None)
            if myrow is None:
                continue
            self.rows[_id] = otherrow + myrow
        return summary

    def __iter__(self):
        for _id in self.rows:
            yield (_id, self.rows[_id])

    def from_csv(self, csvfile):
        with open(csvfile, "r") as fid:
            lines = fid.readlines()
        lines = [x.strip() for x in lines]
        self.headers = lines[0].split(",")
        for line in lines[1:]:
            parts = line.split(",")
            _id = parts[0]
            row = parts[1:]
            self.add_row(_id, row)
