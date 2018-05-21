"""
Simplified Circonus Data Fetching API

This module provides simplified methods for data fetching operations.
To gain access to the full functionality use the circonusapi module.
"""

from circonsapi import circonusapi
import itertools

def _iter_pages(api, method, endpoint, params):
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

class CircData(object):

    def __init__(self, token):
        self.api = circonusapi.CirconusAPI(token)

    def search_metric(self, q):
        """
        Search for metrics. Returns an iterator of metrics matching the query.
        """
        for rec in _iter_pages(self.api, "GET", "/metric", params={"search": q}):
            yield { "name" : rec['_metric_name'], "check_id" : rec["_check"][len('/check/'):]}

    def search_fetch_metric()

            def circ_fetch(check_id, metric, start, period, count, kind="value"):
    """"
    Fetch data from Circonus API
    """
    def post_fetch(r):
        return r.get(kind, None)
    return list(map(post_fetch, circ_api.api_call("GET", "data/{}_{}".format(check_id, metric), params = {
            "period": period,
            "start": int(start), 
            "end": int(start + count * period),
            "format" : "object"
    })['data']))

def circ_fetch_histogram(check_id, metric, start, period, count):
    """"
    Fetch histogram data from Circonus API
    """
    return circ_api.api_call("GET", "data/{}_{}".format(check_id, metric), params = {
            "period": period,
            "start": int(start),
            "end": int(start + (count * period)),
            "format" : "object",
            "type": "histogram",
    })['data']

def circ_search_fetch(q, start, period, count, kind="value"):
    out = {}
    for r in circ_search(q):
        print("fetching", r, file=sys.stderr)
        key  = "{}/{}".format(r['check_id'], r['name'])
        data = circ_fetch(r['check_id'], r['name'], start, period, count, kind=kind)
        out[key] = data
    return out

def caql_fetch(q, start, period, count):
    return circ_api.api_call("GET", "caql", params = {
            "query" : q,
            "period": period,
            "start": int(start), 
            "end": int(start + count * period)
    })
