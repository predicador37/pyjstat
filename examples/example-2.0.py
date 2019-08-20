# -*- coding: utf-8 -*-
""" pyjstat 1.X example for JSON-stat 2.0"""

import time
from pyjstat import pyjstat

EXAMPLE_URL = 'http://www.cso.ie/StatbankServices/StatbankServices.svc/' \
              'jsonservice/responseinstance/TSM01'

# Elapsed time for pyjstat operations only (without network latency)
start = time.time()

# read dataset from url
dataset_from_json_url = pyjstat.Dataset.read(EXAMPLE_URL)

# write dataframe
dataframe = dataset_from_json_url.write('dataframe')
print(dataframe)

# read dataset from dataframe
dataset_from_dataframe = pyjstat.Dataset.read(dataframe)
print(dataset_from_dataframe)

# write dataset to json-stat string
json_string = dataset_from_dataframe.write()
print(json_string)

# read dataset from json-stat string
dataset_from_json_string = pyjstat.Dataset.read(json_string)
print(dataset_from_json_string)

end = time.time()
print("Time: " + str(end - start))
