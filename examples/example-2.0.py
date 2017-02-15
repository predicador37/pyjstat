# -*- coding: utf-8 -*-
from pyjstat import pyjstat
import time
import json



EXAMPLE_URL = 'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/TSM01'
#EXAMPLE_URL = 'http://data.ssb.no/api/v0/dataset/166318.json?lang=en'
dataset = pyjstat.Dataset.read(EXAMPLE_URL)

#dataset = collection.get(0)
df = dataset.to_frame()

print(df)
dataset2 = pyjstat.Dataset.read(df)
start = time.time()
print(json.loads(dataset2.to_json_stat()))

end = time.time()
print("Time: " + str(end - start))
#dataset2 = pyjstat.Dataset.read(df)
#print (dataset2.to_json_stat())
#print (dataset2["value"][4])
