import urllib2
import re
import math
from datetime import datetime
from collections import namedtuple
import operator

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import lxml.html
import pandas as pd

meyrin_url = "http://services.datasport.com/%i/lauf/meyrin/RANG091.HTM"
semi_url = "http://services.datasport.com/%i/lauf/genevema/RANG095.HTM"

f_meyrin_url = "http://services.datasport.com/%i/lauf/meyrin/RANG092.HTM"
f_semi_url = "http://services.datasport.com/%i/lauf/genevema/RANG096.HTM"

def get_data(url, year):
    return urllib2.urlopen(url%(year)).read()

def runners(results_page, matcher, detail=False):
    observations = []
    results_table = lxml.html.fromstring(results_page)
    #lines = results_table.body.find("pre").findall("font")[2].text_content()
    fonts = results_table.body.find("pre").findall("font")
    fonts = [e for e in fonts if e.attrib.get('size', "0")=="2"]
    lines = "".join(e.text_content() for e in fonts)
    lines = [l.strip() for l in lines.split("\r\n")]
    lines = [l for l in lines if l]

    runners = {}
    for line in lines:
        if detail:
            print line.encode('utf-8')

        match = matcher(line, detail)
        if match is not None:
            surname, name, time = match
            if time[0].isnumeric():
                key = surname.encode('utf-8') +" "+name.encode('utf-8')
                if detail:
                    print key, time
                    print "-"*80
                runners[hash(key)] = (time, key)

    return runners

def semier(line, detail=False):
    l = line.split()
    time = l[-6]
    name = l[1]
    surname = l[2]
    if time[0].isnumeric():
        if detail:
            print name.encode('utf-8'), surname.encode('utf-8'), time
            print "-"*80
        return name, surname, time

def meyriner(line, detail=False):
    l = line.split()
    time = l[-5]
    name = l[1]
    surname = l[2]
    if time[0].isnumeric():
        if detail:
            print name.encode('utf-8'), surname.encode('utf-8'), time
            print "-"*80
        return name, surname, time

def seconds(t):
    secs = 0
    if ":" in t:
        secs += int(t[0]) * 60*60
        t = t[2:]
        
    mins = int(t[:2])
    secs += mins*60
    secs += int(t[3]+t[4])
    return secs

def nice_time(x, pos):
    mins, hrs = math.modf(x/3600.)
    secs, mins = math.modf(mins * 60)
    secs *= 60
    if hrs > 0:
        return "%i:%02i.%02i"%(hrs, mins, secs)
    else:
        return "%02i.%02i"%(mins, secs)

    
if __name__ == "__main__":
    meyrin = []
    semi = []
    # Use the foulee of year N to predict for semi in year N+1
    for year in (2010, 2011):
        a = runners(get_data(meyrin_url, year), meyriner, detail=False)
        a.update(runners(get_data(f_meyrin_url, year), meyriner, detail=False))
    
        b = runners(get_data(semi_url, year+1), semier, detail=False)
        b.update(runners(get_data(f_semi_url, year+1), semier, detail=False))
             
        a_ = set(a.keys())
        b_ = set(b.keys())
        both = [(a[runner][1], a[runner][0], b[runner][0]) for runner in a_.intersection(b_)]
        print "In the year", year, len(both), "runners ran both the Foulees and the semi"
        print "Runners sorted by semi marathon time"
        print
        for name, time1, time2 in sorted(both, key=operator.itemgetter(2)):
            print name, time1, time2
            meyrin.append(seconds(time1))
            semi.append(seconds(time2))

    meyrin = np.asarray(meyrin)
    semi = np.asarray(semi)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.hexbin(meyrin, semi, cmap=plt.cm.PuBu)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(nice_time))
    ax.set_xlabel("Foulees automnales de Meyrin 10k")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(nice_time))
    ax.set_ylabel("Geneva half marathon")
                      
    plt.show()
    fig.savefig("/tmp/meyrin-vs-geneva.png")
