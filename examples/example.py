# -*- coding: utf-8 -*-
from pyjstat import pyjstat
import urllib2
import json
from collections import OrderedDict
data = json.load(urllib2.urlopen(
    'http://json-stat.org/samples/oecd-canada.json'),
    object_pairs_hook=OrderedDict)
results = pyjstat.from_json_stat(data)
print results