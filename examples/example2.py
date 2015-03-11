# -*- coding: utf-8 -*-
from pyjstat import pyjstat
import urllib2
import json
from collections import OrderedDict
import pandas as pd

response = pd.read_csv("test_pyjstat.csv")
#print response
result = json.loads(pyjstat.to_json_stat(response),
                               object_pairs_hook=OrderedDict)
print json.dumps(result)
#pyjstat.from_json_stat(json.loads(json.dumps(result),
     #                                               object_pairs_hook=
     #                                              OrderedDict))