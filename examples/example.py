# -*- coding: utf-8 -*-
from pyjstat import pyjstat
import requests
from collections import OrderedDict

data = requests.get('http://json-stat.org/samples/oecd-canada.json')
results = pyjstat.from_json_stat(data.json(object_pairs_hook=OrderedDict))
print (results)
print (pyjstat.to_json_stat(results))
