"""
Simplified Circonus Data Fetching API

This module provides simplified methods for data fetching operations.
To gain access to the full functionality use the circonusapi module.
"""

from circonusapi import circonusapi

FORMAT_FIELDS = [ "count",
    "counter",
    "counter2",
    "counter2_stddev",
    "counter_stddev",
    "derivative",
    "derivative2",
    "derivative2_stddev",
    "derivative_stddev",
    "value" ]

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

class CirconusMetric(object):
    "Circonus Metric class"

    def __init__(self, api, rec):
        self._api = api
        self._check_id = _cid2check_id(rec["_check"])
        self._name = rec['_metric_name']
        self._histogram = rec['_histogram']

    def __str__(self):
        return "Metric{{check_id={},name={},histogram={}}}".format(self._check_id, self._name, self._histogram)

    def __repr__(self):
        return self._check_id + "/" + self._name

    def fetch(self, start, period, count, kind="value"):
        """Fetch numeric data for a metric
        - Fetching multiple fields at once is not supported
        - Data is returned as list of values
        """
        assert(kind in FORMAT_FIELDS)
        params = {
            "period": period,
            "start": int(start),
            "end": int(start + count * period),
            "format": "object",
            "format_fields" : kind,
        }
        endpoint = "data/{}_{}".format(self._check_id, self._name)
        fmt = lambda rec: rec[kind]
        return list(map(fmt, self._api.api_call("GET", endpoint, params=params)['data']))

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
        def fmt(m): return "{:<10} {}".format(m._check_id, m._name)
        return "\n".join([ "check_id   metric_name", "-"*30 ] + list(map(fmt, self)))

class CirconusData(object):
    "Circonus data fetching class"

    def __init__(self, token):
        self.api = circonusapi.CirconusAPI(token)

    def search(self, search="", kind=None):
        "Iterate over all metrics matching search"
        params = {"search": search}
        fmt = lambda rec: CirconusMetric(self.api, rec)
        return CirconusMetricList(map(fmt, _iter_pages(self.api, "GET", "/metric", params=params)))
