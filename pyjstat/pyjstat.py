# -*- coding: utf-8 -*-
import urllib2
import logging
import httplib
import inspect
import json
import math
from operator import mul
import numpy as np
import pandas as pd
from collections import OrderedDict
import httplib2
from bs4 import BeautifulSoup

#BASE_URL = "http://json-stat.org/samples/oecd-canada.json"
# TODO: handle dataset with no values
# BASE_URL = "http://json-stat.org/samples/hierarchy.json" 
#BASE_URL = "http://json-stat.org/samples/us-gsp.json"
#BASE_URL = "http://json-stat.org/samples/us-labor.json"
#BASE_URL = "http://json-stat.org/samples/us-unr.json"
#BASE_URL = "http://json-stat.org/samples/order.json"
#BASE_URL = "http://data.ssb.no/api/v0/dataset/26940.json?lang=en"
#BASE_URL = "http://data.ssb.no/api/v0/dataset/62495.json?lang=en"
BASE_URL = "http://data.ssb.no/api/v0/dataset/26944.json?lang=en"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_input(naming):
    if naming not in ['label','id']:
        raise ValueError('naming must be "label" or "id"')

def get_dim_label(jsList, thisDim):
    
    try:
        thisDimLabel = jsList['dimension'][thisDim]['category']['label']    
    except KeyError:
        thisDimIndex = get_dim_index(jsList, thisDim)
        thisDimLabel = pd.concat([thisDimIndex['id'], thisDimIndex['id']], axis=1)
        thisDimLabel.columns = ['id', 'label']   
    else:
        thisDimLabel = pd.DataFrame(zip(thisDimLabel.keys(),
                                        thisDimLabel.values()),
                                        index = thisDimLabel.keys(),
                                        columns=['id','label'])
    return thisDimLabel

def get_dim_index(jsList, thisDim):
    try:
        thisDimIndex = jsList['dimension'][thisDim]['category']['index']
    except KeyError:
        thisDimLabel = get_dim_label(jsList, thisDim)
        thisDimIndex = pd.DataFrame(zip([thisDimLabel['id'][0]],[0]), 
                                    index=[1],
                                    columns=['id','index'])
    else:
        if type(thisDimIndex) is list:
            thisDimIndex = pd.DataFrame(zip(thisDimIndex,
                                            range(0,len(thisDimIndex))),
                                        index = thisDimIndex,
                                        columns=['id','index'])
        else:
            thisDimIndex = pd.DataFrame(zip(thisDimIndex.keys(),
                                            thisDimIndex.values()),
                                        index = thisDimIndex.keys(),
                                        columns = ['id','index'])
    return thisDimIndex                                                              

def from_JSON_stat(x, naming='label'):
    check_input(naming)
    for element in x:
        jsList = x[element]
        dimSizes = jsList['dimension']['size']
        dimensions = []
        dimNames = []
        numDims = len(dimSizes)
        
        baseSys = []
        for i in range(0,numDims+1):
            baseSys.append(reduce(mul, dimSizes[i:numDims+1],1))
        for i in range(0,numDims):
            thisDim = jsList['dimension']['id'][i]
           
            thisDimName = jsList['dimension'][thisDim]['label']
            
            if not thisDimName:
                thisDimName = thisDim
            thisDimSize = jsList['dimension']['size'][i]
            thisDimIndex = get_dim_index(jsList, thisDim)
            thisDimLabel = get_dim_label(jsList, thisDim)
            thisDimAll = pd.merge(thisDimIndex, thisDimLabel)     
           
            #print thisDimIndex                        
            #print thisDimAll
            if (naming == 'label'):
                dimensions.append(thisDimAll['label'])
                dimNames.append(thisDimName)
            else:
                dimensions.append(thisDimAll['id'])
                dimNames = thisDim
           
        thisN = len(jsList['value'])
        output = pd.DataFrame(columns=dimNames + [unicode("value", "utf-8")], index=range(1,thisN)) 
        theseVals = jsList['value']
        if type(theseVals) is dict: #see json-stat docs
            maxVal = max(theseVals.keys(), key=int)
            vals = []
            for element in theseVals:
                for i in range (0,maxVal):
                    if element.key == i:
                        vals.append(element.value)
                    else:
                        vals.append(None)
            theseVals = vals
        indices = range(0,len(theseVals))
  
        for i in range(0,thisN):
            value = theseVals[i]
            index = indices[i]
            output.loc[i+1] = [math.floor((index)/baseSys[j+1])%dimSizes[j] for j in range(0,numDims)] + [value]
       
        
   
   
        for i in range(0,numDims):
            output.ix[:,i] = list(dimensions[i][output.ix[:,i]])
   
        print "output " 
        print str(output) 
        
    
def main():
    
   
    uri_list = urllib2.urlopen("http://data.ssb.no/api/v0/dataset/list.json?lang=en")
    ds_list = json.loads(uri_list.read(), object_pairs_hook=OrderedDict)
    uri_list.close()
    test_links = []
    for element in ds_list['datasets']:
        test_links.append(element['jsonURI'])
    
    print "Testing " + str(len(test_links)) + " links"
     
    for link in test_links:  
        print "Testing link: " + str(link)
        request = urllib2.Request(link,
                                  headers={"Accept": "application/json"})
        try:
            f = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            logger.error((inspect.stack()[0][3]) +
                          ': HTTPError = ' + str(e.code) +
                          ' ' + str(e.reason) +
                          ' ' + str(e.geturl()))
            raise
        except urllib2.URLError, e:
            logger.error('URLError = ' + str(e.reason) +
                         ' ' + str(e.geturl()))
            raise
        except httplib.HTTPException, e:
            logger.error('HTTPException')
            raise
        except Exception:
            import traceback
            logger.error('Generic exception: ' + traceback.format_exc())
            raise
        else:
            response = json.loads(f.read(), object_pairs_hook=OrderedDict)
            f.close()
    
        from_JSON_stat(response)
    
   
  
    
    
if __name__ == '__main__':
    main()