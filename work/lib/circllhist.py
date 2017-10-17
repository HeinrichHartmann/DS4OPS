#
# Some functions to handle Circonus log linar histograms
#

import math
from scipy import stats
import numpy as np
from collections import defaultdict

def merge(hists):
    H=defaultdict(int)
    for h in hists:
        for b,c in h.items():
            H[b]+=c
    return H

def bin_width(b):
    if b == 0: return 0
    s = 1 if (b >= 0) else -1
    b = float(b * s)
    p = math.floor(math.log10(b))
    return 10 ** (p - 1)

def count(h):
    n = 0
    for b, c in h.items():
        n += c
    return n

# generate samples from histogram

def sample_bin(b):
    b = float(b)
    s = 1 if (b >= 0) else -1
    return s*stats.uniform.rvs(s*b, bin_width(s*b))
    
def sample_hist(h):
    "For each each bin b draw h[b] samples"
    out = []
    for b, c in h.items():
        for _ in range(c):
            out.append(sample_bin(b))
    return out

def sample(h, N):
    "Draw N samples from histogram"
    C=count(h)
    K=list(h.keys())
    P=list(map(lambda k:h[k]/C, K))
    out = []
    if len(K) == 0: return out
    for _ in range(N):
        b = np.random.choice(K, p=P)
        out.append(sample_bin(b))
    return out

def bootstrap(h):
    "Draw count(h) samples from total histogram"
    return sample(h, count(h))

def flatten(h):
    out = []
    for b, c in h.items():
        b = float(b)
        for _ in range(c):
            out.append(b)
    return out
