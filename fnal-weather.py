import urllib2
from datetime import datetime
from collections import namedtuple

import lxml.html
import pandas as pd

base_url = "http://www-esh.fnal.gov/pls/default/weather.month?this_year=%i&this_month=%01i"

#['05/30/1994', '0.00', '75.0', '59.4', '60.2', '305', '6.3', '203.1', '59.0', '50.5', '87.8', '65.1', '83.6', '20.8']

Day = namedtuple("Day", 'date avg_temp min_temp max_temp')

def get_month(month, year):
    return urllib2.urlopen(base_url%(year, month)).read()

def get_may_data(year):
    observations = []
    may = lxml.html.fromstring(get_month(5, year))
    days = may.body.findall("table")[1]
    for day in days:
        fields = day.text_content().split()
        
        # first three rows are headers, skip them
        if fields[0].isalpha():
            continue

        try:
            observations.append(dict(date=datetime.strptime(fields[0], "%m/%d/%Y"),
                                     avg_temp=float(fields[2]),
                                     min_temp=float(fields[8]),
                                     max_temp=float(fields[10]),
                                     )
                                )

        except:
            print year, fields
        
    return observations


if __name__ == "__main__":
    obs = []
    for year in (1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001,
                 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
                 2010, 2011, 2012):
        obs += get_may_data(year)

    import pickle
    pickle.dump(obs, file("fnal-weather.pickle", "wb"))
    
    
