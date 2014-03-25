# -*- coding: utf-8 -*-
import urllib2
import logging
import httplib
import inspect
import json
import math
from operator import mul
import pandas as pd
from collections import OrderedDict


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
BASE_TEST_URL = "http://data.ssb.no/api/v0/dataset/list.json?lang=en"
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def check_input(naming):
    
    """Checks and validates input params.

    Args:
      naming (string): a string containing the naming type (label or index)
     
    Returns:
      Nothing

    Raises:
      ValueError: if the parameter is not in the allowed list.

    """
    
    if naming not in ['label','id']:
        raise ValueError('naming must be "label" or "id"')

def get_dim_label(js_dict, dim):
    
    """Gets label from a given dimension.

    Args:
      js_dict (dict): dictionary containing dataset data and metadata.
      dim (string): dimension name obtained from JSON file.
    Returns:
      dim_label(pandas.DataFrame): DataFrame with label-based dimension data.

    """
    
    try:
        dim_label = js_dict['dimension'][dim]['category']['label']    
    except KeyError:
        dim_index = get_dim_index(js_dict, dim)
        dim_label = pd.concat([dim_index['id'],
                               dim_index['id']],
                              axis = 1)
        dim_label.columns = ['id', 'label']   
    else:
        dim_label = pd.DataFrame(zip(dim_label.keys(),
                                     dim_label.values()),
                                 index = dim_label.keys(),
                                 columns=['id', 'label'])
    return dim_label

def get_dim_index(js_dict, dim):

    """Gets index from a given dimension.

    Args:
      js_dict (dict): dictionary containing dataset data and metadata.
      dim (string): dimension name obtained from JSON file.
    Returns:
      dim_index(pandas.DataFrame): DataFrame with index-based dimension data.

    """
    
    try:
        dim_index = js_dict['dimension'][dim]['category']['index']
    except KeyError:
        dim_label = get_dim_label(js_dict, dim)
        dim_index = pd.DataFrame(zip([dim_label['id'][0]], [0]), 
                                 index=[1],
                                 columns=['id', 'index'])
    else:
        if type(dim_index) is list:
            dim_index = pd.DataFrame(zip(dim_index,
                                         range(0, len(dim_index))),
                                     index = dim_index,
                                     columns=['id', 'index'])
        else:
            dim_index = pd.DataFrame(zip(dim_index.keys(),
                                         dim_index.values()),
                                     index = dim_index.keys(),
                                     columns = ['id', 'index'])
    return dim_index

def from_json_stat(data, naming='label'):
    
    """Converts JSON-stat format into pandas.DataFrame object

    Args:
      data(string): data in JSON-stat format to convert.
      naming(string): dimension naming. Possible values: 'label' or 'index'
    Returns:
      output(pandas.DataFrame): DataFrame with imported data.

    """
    
    check_input(naming)
    for element in data:
        js_dict = data[element]
        dim_sizes = js_dict['dimension']['size']
        dimensions = []
        dim_names = []
        dim_num = len(dim_sizes) 
        base_sys = []
        for i in range(0, dim_num):
            base_sys.append(reduce(mul, dim_sizes[i:dim_num], 1))
        #for i in range(0, dim_num):
            dim = js_dict['dimension']['id'][i]
           
            dim_name = js_dict['dimension'][dim]['label']
            
            if not dim_name:
                dim_name = dim
            #dim_size = js_list['dimension']['size'][i]
            dim_index = get_dim_index(js_dict, dim)
            dim_label = get_dim_label(js_dict, dim)
            dim_all = pd.merge(dim_index, dim_label)     
         
            if (naming == 'label'):
                dimensions.append(dim_all['label'])
                dim_names.append(dim_name)
            else:
                dimensions.append(dim_all['id'])
                dim_names = dim
           
        total_n = len(js_dict['value'])
        output = pd.DataFrame(columns=dim_names + [unicode('value', 'utf-8')], 
                              index=range(1, total_n)) 
        values = js_dict['value']
        if type(values) is dict: #see json-stat docs
            max_val = max(values.keys(), key = int)
            vals = []
            for element in values:
                for i in range (0, max_val):
                    if element.key == i:
                        vals.append(element.value)
                    else:
                        vals.append(None)
            values = vals
        indices = range(0, len(values))
  
        for i in range(0, total_n):
            value = values[i]
            index = indices[i]
            output.loc[i + 1] = [math.floor((index) / base_sys[j])\
                                 % dim_sizes[j] for j in range(0, dim_num)] +\
                                [value]
       
        
   
   
        for i in range(0, dim_num):
            output.ix[:, i] = list(dimensions[i][output.ix[:, i]])
   
        print "output " 
        print str(output) 
        
    
def main():
    
    
    uri_list = urllib2.urlopen(BASE_TEST_URL)
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
            requested_data = urllib2.urlopen(request)
        except urllib2.HTTPError, ex:
            LOGGER.error((inspect.stack()[0][3]) +
                          ': HTTPError = ' + str(ex.code) +
                          ' ' + str(ex.reason) +
                          ' ' + str(ex.geturl()))
            raise
        except urllib2.URLError, ex:
            LOGGER.error('URLError = ' + str(ex.reason) +
                         ' ' + str(ex.geturl()))
            raise
        except httplib.HTTPException, ex:
            LOGGER.error('HTTPException')
            raise
        except Exception:
            import traceback
            LOGGER.error('Generic exception: ' + traceback.format_exc())
            raise
        else:
            response = json.loads(requested_data.read(),
                                  object_pairs_hook=OrderedDict)
            requested_data.close()
    
        from_json_stat(response)

if __name__ == '__main__':
    main()