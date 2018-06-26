# Preamble

import json
import os
import math
from datetime import datetime
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt

from circonusapi import circonusdata

with open(os.path.expanduser("/work/.circonusrc.json"),"r") as fh:
    config = json.load(fh)

def hist_plot(H,**kwargs):
    x=[] # midpoints
    h=[] # height
    w=[] # widths
    for b, c in H:
        x.append(b.midpoint())
        h.append(c / b.width())
        w.append(b.width())
    return plt.bar(x,h,w,**kwargs)

def caql_plot(account, *args,**kwargs):
    circ = circonusdata.CirconusData(config[account])
    data=circ.caql(*args)
    df=pd.DataFrame(data)
    df['time']=pd.to_datetime(df['time'],unit='s')
    df.set_index('time', inplace=True)
    return df.plot(figsize=(20,5), legend=False, lw=.8, **kwargs)

def caql_hist_plot(account, *args, **kwargs):
    fig=plt.figure(figsize=(20,5))
    circ = circonusdata.CirconusData(config[account])
    data=circ.caql(*args)
    for H in data['output[0]']:
        hist_plot(H, alpha=0.2, **kwargs)
    return fig.get_axes()[0]
