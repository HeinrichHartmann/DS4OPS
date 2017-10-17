#
# Simplified Circonus Data Fetching API
#

import sys
from circonusapi import circonusapi
import pandas as pd
import math

class api:

    def __init__(self, token):
        self.token = token
        self.api = circonusapi.CirconusAPI(token)

    def search(self, q, **kwargs):
        def post_search(r):
            return { "name" : r['_metric_name'], "check_id" : r["_check"][len('/check/'):] }
        return list(map(post_search,
                    self.api.api_call("GET","/metric", params={"search": q, **kwargs})
                   ))

    def fetch(self, check_id, metric, start, period, count):
        """
        Fetch data from Circonus API
        """
        def post_fetch(r):
            return r.get('value', None)
        out = list(map(post_fetch, self.api.api_call("GET", "data/{}_{}".format(check_id, metric), params = {
            "period": period,
            "start": int(start),
            "end": int(start + count * period),
            "format" : "object"
        })['data']))
        return out + [None] * (count - len(out)) # extend length if needed

    def search_fetch(self, q, start, period, count, **kwargs):
        out = {}
        for r in self.search(q, **kwargs):
            print("fetching", r, file=sys.stderr)
            key  = "{}/{}".format(r['check_id'], r['name'])
            data = self.fetch(r['check_id'], r['name'], start, period, count)
            out[key] = data
        return out

    def search_fetch_tsdf(self, q, start, period, count, **kwargs):
        X = self.search_fetch(q, start, period, count, **kwargs)
        idx = [ pd.to_datetime(start + period * n, unit='s') for n in range(count) ]
        return pd.DataFrame(X, index=idx)
