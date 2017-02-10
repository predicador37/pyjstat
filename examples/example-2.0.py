# -*- coding: utf-8 -*-
from pyjstat import pyjstat
import requests
from collections import OrderedDict
import json

EXAMPLE_URL = 'http://json-stat.org/samples/oecd.json'

dataset = pyjstat.Dataset.read(EXAMPLE_URL)
df = dataset.to_frame()
print(df)
dataset2 = pyjstat.Dataset.read(df)
print (dataset2.to_json_stat())
print (dataset2["value"][4])
