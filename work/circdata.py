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

def _log(**args):
    import json
    print(json.dumps(args))

def _cid2check_id(s):
    return s[len('/check/'):]

def _iter_pages(api, method, endpoint, params={}):
    "Merge paginated results into a single iterator"
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

    def name(self):
        return self._name

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
        _log(event="HTTP", endpoint=endpoint, count=count, kind=kind)
        return list(map(fmt, self._api.api_call("GET", endpoint, params=params)['data']))

class CirconusCheck(object):
    "Circonus Check class"

    def __init__(self, api, rec):
        self._api = api
        self._check_id = _cid2check_id(rec['_cid'])
        self._check_uuid = rec['_check_uuid']
        self._check_bundle = rec['_check_bundle']

    def __str__(self):
        return "Check{{check_id={},check_uuid={}}}".format(self._check_id, self._check_uuid)

    def metrics(self, search=""):
        "Iterate over all metrics within the check"
        params = { "search" : "(check_id:{})".format(self._check_id) + (search or "") }
        fmt = lambda rec: CircMetric(self._api, rec)
        return map(fmt, _iter_pages(self._api, "GET", "/metric", params=params))

class CirconusData(object):
    "Circonus data fetching class"

    def __init__(self, token):
        self.api = circonusapi.CirconusAPI(token)

    def checks(self, search=""):
        "Iterate over all checks (matching search)"
        params = {"search": search}
        fmt = lambda rec: CircCheck(self.api, rec)
        return map(fmt, _iter_pages(self.api, "GET", "/check", params=params))

    def metrics(self, search="", kind=None):
        "Iterate over all metrics (matching search)"
        params = {"search": search}
        fmt = lambda rec: CircMetric(self.api, rec)
        return map(fmt, _iter_pages(self.api, "GET", "/metric", params=params))

#     def search_fetch_metric()

#             def circ_fetch(check_id, metric, start, period, count, kind="value"):
#     """"
#     Fetch data from Circonus API
#     """
#     def post_fetch(r):
#         return r.get(kind, None)
#     return list(map(post_fetch, )

# def circ_fetch_histogram(check_id, metric, start, period, count):
#     """"
#     Fetch histogram data from Circonus API
#     """
#     return circ_api.api_call("GET", "data/{}_{}".format(check_id, metric), params = {
#             "period": period,
#             "start": int(start),
#             "end": int(start + (count * period)),
#             "format" : "object",
#             "type": "histogram",
#     })['data']

# def circ_search_fetch(q, start, period, count, kind="value"):
#     out = {}
#     for r in circ_search(q):
#         print("fetching", r, file=sys.stderr)
#         key  = "{}/{}".format(r['check_id'], r['name'])
#         data = circ_fetch(r['check_id'], r['name'], start, period, count, kind=kind)
#         out[key] = data
#     return out

# def caql_fetch(q, start, period, count):
#     return circ_api.api_call("GET", "caql", params = {
#             "query" : q,
#             "period": period,
#             "start": int(start),
#             "end": int(start + count * period)
#     })
