# -*- coding: utf-8 -*-
from pyjstat import pyjstat
import requests
from collections import OrderedDict
import json

EXAMPLE_URL = 'http://json-stat.org/samples/us-labor-ds.json'

data = requests.get(EXAMPLE_URL)
results = pyjstat.from_json_stat(data.json(object_pairs_hook=OrderedDict))
print (results)
print (json.dumps(json.loads(pyjstat.to_json_stat(results))))
