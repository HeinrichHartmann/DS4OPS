"""
Simplified Circonus Data Fetching API

This module provides simplified methods for data fetching operations.
To gain access to the full functionality use the circonusapi module.
"""

import math
from datetime import datetime
from itertools import islice

from circonusapi import circonusapi
from circllhist import Circllhist

FORMAT_FIELDS = [
    "count",
    "counter",
    "counter2",
    "counter2_stddev",
    "counter_stddev",
    "derivative",
    "derivative2",
    "derivative2_stddev",
    "derivative_stddev",
    "value",
    "stddev",
    "histogram" ]
HIST_STATES = ["active", "true"]
NAN = float('nan')
BIG_INT=2**64-1

################################################################################
## Helper Functions

def _cid2check_id(cid):
    return cid[len('/check/'):]

def _iter_pages(api, method, endpoint, params=None, limit=BIG_INT):
    "Merge paginated results into a single iterator"
    params = params or {}
    _from = 0
    _size = min(1000, limit)
    _count = 0
    while True:
        params["size"] = _size
        params["from"] = _from
        res = api.api_call(method, endpoint, params=params)
        if not res:
            break
        for r in res:
            _count += 1
            if _count > limit:
                break
            yield r
        _from += _size

def _hist2kind(hist, kind):
    if kind == "histogram":
        return hist
    if kind == "value":
        return hist.mean()
    if kind == "count":
        return hist.count()
    if kind == "stddev":
        return hist.stddev()
    return NAN

def _extend(kind, count, lst):
    if kind == "histogram":
        lst += [ Circllhist() for i in range(count - len(lst)) ]
        return lst
    else:
        for i, y in enumerate(lst):
            if not y:
                lst[i] = NAN
        lst += [NAN]*(count - len(lst))
        return lst

def _caql_infer_type(res):
    if len(res[0]) >= 3 and type(res[0][2]) == dict:
        return "histogram"
    else:
        return "numeric"

def _fix_time(start, period):
    if type(start) == datetime:
        return _fix_time(start.timestamp(), period)
    if not start % period == 0:
        raise Exception(
            "start parameter {} is not divisible by period {}. Use e.g. {} instead.".format(
                start, period, math.floor(start/period)
            ))
    return start

################################################################################
## Classes

def CirconusMetricFactory(api, rec):
    "Create a suitable CirconusMetric object from an API result"
    check_id = _cid2check_id(rec["_check"])
    name = rec['_metric_name']
    if rec['_histogram'] in HIST_STATES:
        return CirconusMetricHistogram(api, check_id, name)
    return CirconusMetricNumeric(api, check_id, name)

class CirconusMetric(object):
    "Circonus Metric base class"

    def __init__(self, api, check_id, name):
        self._api = api
        self._check_id = check_id
        self._name = name

    def __repr__(self):
        return "CirconusMetric{{check_id={},name={}}}".format(self._check_id, self._name)

    def name(self):
        return self._name

    def check_id(self):
        return self._check_id

class CirconusMetricNumeric(CirconusMetric):

    def type(self):
        return "numeric"

    def fetch(self, start, period, count, kind):
        "Fetch data from a numeric metric"
        assert(kind in FORMAT_FIELDS)
        if kind == "histogram":
            def fmt(rec):
                # raise Exception("Can't fetch histogram data from a numeric metric")
                h = Circllhist()
                if rec[kind]:
                    h.insert(rec[kind])
                return h
        else:
            def fmt(rec): return rec[kind]
        params = {
            "type" : "numeric",
            "period": period,
            "start": int(start),
            "end": int(start + count * period),
            "format": "object",
            "format_fields" : kind,
        }
        endpoint = "data/{}_{}".format(self._check_id, self._name)
        return _extend(kind, count, list(map(fmt, self._api.api_call("GET", endpoint, params=params)['data'][:count])))

class CirconusMetricHistogram(CirconusMetric):

    def type(self):
        return "histogram"

    def fetch(self, start, period, count, kind):
        "Fetch data from a histogram metric"
        assert(kind in FORMAT_FIELDS)
        params = {
            "type" : "histogram",
            "period": period,
            "start": int(start),
            "end": int(start + count * period),
            "format": "object",
        }
        def fmt(rec): return _hist2kind(Circllhist.from_dict(rec[2]), kind)
        endpoint = "data/{}_{}".format(self._check_id, self._name)
        return _extend(kind, count, list(map(fmt, self._api.api_call("GET", endpoint, params=params)['data'][:count])))

class CirconusMetricList(list):
    """Holds multiple Circonus Metrics.
    - Can be used like a list to access the individual member metrics
    - __str__() returns a table formatted table representation
    - fetch() can be used to fetch data
    """

    def fetch(self, start, period, count, kind="value"):
        """
        Fetch data from all metrics in the list.
        Return result as map: metric_name => list
        Fetches are done serially. Use CAQL for parallel data fetching.
        """
        start = _fix_time(start, period)
        out = {}
        out['time'] = [ start + n * period for n in range(count) ]
        for metric in self:
            key = "{}/{}".format(metric.check_id(), metric.name())
            out[key] = metric.fetch(start, period, count, kind)
        return out

    def __repr__(self):
        return "CirconusMetricList(len={})".format(len(self))

    def __str__(self):
        "Print metric List as table"
        def fmt(m): return "{:<10} {:<10} {:<50}".format(m.check_id(), m.type(), m.name())
        return "\n".join([ "check_id   type       metric_name", "-"*50 ] + list(map(fmt, self)))


class CirconusData(object):
    "Circonus data fetching class"

    def __init__(self, token):
        self._api = circonusapi.CirconusAPI(token)

    def search(self, search="", kind=None, limit=BIG_INT):
        """Search for metrics using the metric search API.
        Returns a CirconusMetricList Object, that can be used to fetch data.
        """
        params = {"search": search}
        fmt = lambda rec: CirconusMetricFactory(self._api, rec)
        return CirconusMetricList(map(fmt, _iter_pages(self._api, "GET", "/metric", params=params, limit=limit)))

    def caql(self, query, start, period, count):
        """
        Fetch data using CAQL.
        Returns a map: slot_name => list
        Limitations:
        - slots_names are currently output[i]
        - For histogram output only a single slot is returned
        """
        start = _fix_time(start, period)
        params = {
            "query": query,
            "period": period,
            "start": int(start),
            "end": int(start + count * period),
        }
        res = self._api.api_call("GET", "/caql", params=params)['_data']
        if _caql_infer_type(res) == "histogram":
            # In this case, we have only a single output metric and res looks like:
            # res = [[1467892920, 60, {'1.2e+02': 1, '2': 1, '1': 1}], ... ]
            return {
                'time' : [ row[0] for row in res ],
                'output[0]' : [ Circllhist.from_dict(row[2]) for row in res ],
            }
        else:
            # In the numeric case res looks like this:
            # res = [[1467892920, [1, 2, 3]], [1467892980, [1, 2, 3]], ... ]
            out = {}
            width = len(res[0][1])
            out['time'] = [ row[0] for row in res ]
            for i in range(width):
                out['output[{}]'.format(i)] = [ row[1][i] for row in res ]
            return out
