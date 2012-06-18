"""Experiments to get the route of the olympic torch around the UK in 2012"""

import json
import pprint
import urllib
import urllib2


events_url = "http://mappingdata.london2012.com/torchevents/byarea"
params = {'datasetId': 'TorchRoute-59da3655-1856-4244-b225-38b8420421db',
          'top': '61.53228',
          'left': '-16.91897',
          'bottom': '43.59495',
          'right': '13.66697',
          'zoomLevel': '11',
          }

url = (events_url + "?" + urllib.urlencode(params) + "&" +
       urllib.urlencode({'eventTypes': 1}) + "&" +
       urllib.urlencode({'eventTypes': 2}) + "&" +
       urllib.urlencode({'eventTypes': 3}) + "&" +
       urllib.urlencode({'eventTypes': 5})
       )
       
# They don't understand POST, just GET
req = urllib2.Request(url)
print req.get_full_url()
req.add_header("User-Agent", "Mozilla")
req.add_header("Host", "mappingdata.london2012.com")
req.add_header("Accept", "*/*")

r = urllib2.urlopen(req)    
text = r.read()

events = json.loads(text)

pprint.pprint(events)
print len(events)
