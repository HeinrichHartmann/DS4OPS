"""
Simplified Circonus Data Fetching API

This module provides simplified methods for data fetching operations.
To gain access to the full functionality use the circonusapi module.
"""

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

def _cid2check_id(cid):
    return cid[len('/check/'):]

def _iter_pages(api, method, endpoint, params=None):
    "Merge paginated results into a single iterator"
    params = params or {}
    _from = 0
    _size = 100
    while True:
        params["size"] = _size
        params["from"] = _from
        res = api.api_call(method, endpoint, params=params)
        if not res: break
        for r in res:
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
    # else:
    for i, y in enumerate(lst):
        if not y:
            lst[i] = NAN
    lst += [NAN]*(count - len(lst))
    return lst

def CirconusMetricFactory(api, rec):
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

    def __str__(self):
        return "CirconusMetric{{check_id={},name={}}}".format(self._check_id, self._name)

    def __repr__(self):
        return self._check_id + "/" + self._name

    def name(self):
        return self._name

    def check_id(self):
        return self._check_id

class CirconusMetricNumeric(CirconusMetric):

    def type(self):
        return "numeric"

    def fetch(self, start, period, count, kind="value"):
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
        return _extend(kind, count, list(map(fmt, self._api.api_call("GET", endpoint, params=params)['data'][:20])))

class CirconusMetricHistogram(CirconusMetric):

    def type(self):
        return "histogram"

    def fetch(self, start, period, count, kind="value"):
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
        return _extend(kind, count, list(map(fmt, self._api.api_call("GET", endpoint, params=params)['data'][:20])))

class CirconusMetricList(list):
    "Holds multiple metrics"

    def fetch(self, *args, **kwargs):
        "Fetch all metrics, return result as map"
        return {
            repr(metric) : metric.fetch(*args, **kwargs)
            for metric in self
        }

    def __repr__(self):
        return "CirconusMetricList" + str(list(self))

    def __str__(self):
        "print metric List as table"
        def fmt(m): return "{:<10} {:<10} {:<50}".format(m.check_id(), m.type(), m.name())
        return "\n".join([ "check_id   type       metric_name", "-"*50 ] + list(map(fmt, self)))

class CirconusData(object):
    "Circonus data fetching class"

    def __init__(self, token):
        self.api = circonusapi.CirconusAPI(token)

    def search(self, search="", kind=None):
        "Iterate over all metrics matching search"
        params = {"search": search}
        fmt = lambda rec: CirconusMetricFactory(self.api, rec)
        return CirconusMetricList(map(fmt, _iter_pages(self.api, "GET", "/metric", params=params)))
