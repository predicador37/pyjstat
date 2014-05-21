# -*- coding: utf-8 -*-
import urllib2
import json
from pyjstat import pyjstat
    
results = pyjstat.from_json_stat(json.load(urllib2.urlopen(
                             'http://json-stat.org/samples/oecd-canada.json')))
print results
print pyjstat.to_json_stat(results)
