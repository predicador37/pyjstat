# -*- coding: utf-8 -*-
from collections import OrderedDict

from pyjstat import pyjstat
import time
import json



EXAMPLE_URL = 'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/TSM01'
#EXAMPLE_URL = 'http://data.ssb.no/api/v0/dataset/166318.json?lang=en'
dataset = pyjstat.Dataset.read(EXAMPLE_URL)
#dataset = collection.get(0)
df = dataset.write('dataframe')

print(df)
dataset2 = pyjstat.Dataset.read(df)
print(dataset2['version'])
start = time.time()
print(dataset2.write())

json_data = json.loads(dataset2.write(),object_pairs_hook=OrderedDict)
print(json_data)



end = time.time()
print("Time: " + str(end - start))
#dataset2 = pyjstat.Dataset.read(df)
#print (dataset2.to_json_stat())
#print (dataset2["value"][4])
