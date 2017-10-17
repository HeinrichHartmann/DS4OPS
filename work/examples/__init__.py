import requests
from requests.compat import quote

def graphite_fetch(target, start, until, count=None):
    """
    Simple get taget from locally hosted graphite
    """
    url = 'https://localhost/render/?target=%s&from=%s&until=%s&format=json' % (
        quote(target),
        quote(start),
        quote(until)
    )
    response = requests.get(url, verify=False)
    result = response.json()[0]
    if count is not None:
        return {
            'target': result['target'],
            'datapoints': result['datapoints'][:count]
        }
    return result
