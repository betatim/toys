import urllib2
import re
import math
from datetime import datetime
from collections import namedtuple
import operator
import pdb

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import lxml.html
import pandas as pd


cyclo_url = "http://services.datasport.com/%s/velo/cycloleman/RANG011.HTM"


def get_data(url, year):
    return urllib2.urlopen(url%(year)).read()

def cyclists(results_page, matcher, detail=False):
    observations = []
    results_table = lxml.html.fromstring(results_page)
    #lines = results_table.body.find("pre").findall("font")[2].text_content()
    fonts = results_table.body.find("pre").findall("font")
    fonts = [e for e in fonts if e.attrib.get('size', "0")=="2"]
    lines = "".join(e.text_content() for e in fonts)
    lines = [l.strip() for l in lines.split("\r\n")]
    lines = [l for l in lines if l]

    cyclists = []
    for line in lines:
        if detail:
            print line.encode('utf-8')

        match = matcher(line, detail)
        if match is not None:
            name, surname, time = match
            if time[0].isnumeric():
                key = name.encode('utf-8') +" "+ surname.encode('utf-8')
                if detail:
                    print key, time
                    print "-"*80
                cyclists.append((key, seconds(time)))

    return cyclists

def cycloer(year):
    def match(line, detail=False):
        l = line.split()
        if detail:
            print l

        name = l[1]
        surname = l[2]
            
        if year == 2010:
            time = l[-4]
        else:
            time = l[-5]
                        
        if time[0].isnumeric():
            if detail:
                print name.encode('utf-8'), surname.encode('utf-8'), time

            return name, surname, time

    return match

def seconds(t):
    secs = 0
    if ":" in t:
        secs += int(t[0]) * 60*60
        t = t[2:]
        
    mins = int(t[:2])
    secs += mins*60
    secs += int(t[3]+t[4])
    return secs

def nice_time(x, pos=0):
    mins, hrs = math.modf(x/3600.)
    secs, mins = math.modf(mins * 60)
    secs *= 60
    if hrs > 0:
        return "%i:%02i.%02i"%(hrs, mins, secs)
    else:
        return "%02i.%02i"%(mins, secs)

    
if __name__ == "__main__":
    cycle = []
    detail = False
    axes = []
    
    for year in (2012, 2013):
        a = cyclists(get_data(cyclo_url, year), cycloer(year), detail=detail)

        times = np.asarray([k[1] for k in a])
        df = pd.DataFrame.from_records(a, columns=['name', 'time'])

        if not axes:
            ax = df.time.hist(bins=60, range=(3.5*60*60, 9.*60*60), alpha=0.7)
        else:
            ax = df.time.hist(bins=60, range=(3.5*60*60, 9.*60*60), alpha=0.7,
                              ax=axes[-1])
            
        axes.append(ax)
        ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(nice_time))

        b = np.histogram(df.time, bins=60, range=(3.5*60*60, 9.*60*60))
        a = b[0]/float(sum(b[0]))
        print year, "Ten fastest times:", [nice_time(x) for x in list(sorted(times))[:10]]
        print year, "Top 25% finish in:", nice_time(b[1][a.cumsum()>0.25][0], 0)
        print year, "Mean and median time:", nice_time(times.mean()), nice_time(np.median(times))

    ax.legend([2010, 2011, 2012])
    plt.show()
    
    xxx="""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.hexbin(meyrin, semi, cmap=plt.cm.PuBu)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(nice_time))
    ax.set_xlabel("Foulees automnales de Meyrin 10k")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(nice_time))
    ax.set_ylabel("Geneva half marathon")
                      
    plt.show()
    fig.savefig("/tmp/meyrin-vs-geneva.png")"""
