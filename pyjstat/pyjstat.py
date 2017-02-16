# -*- coding: utf-8 -*-
"""pyjstat is a python module for JSON-stat formatted data manipulation.

This module allows reading and writing JSON-stat [1]_ format with python,
using data frame structures provided by the widely accepted
pandas library [2]_. The JSON-stat format is a simple lightweight JSON format
for data dissemination. Pyjstat is inspired in rjstat [3]_, a library to read
and write JSON-stat with R, by ajschumacher.

pyjstat is written and maintained by `Miguel Expósito Martín
<https://twitter.com/predicador37>`_ and is distributed under the Apache 2.0
License (see LICENSE file).

.. [1] http://json-stat.org/ for JSON-stat information
.. [2] http://pandas.pydata.org for Python Data Analysis Library information
.. [3] https://github.com/ajschumacher/rjstat for rjstat library information

Example:
  Importing a JSON-stat file into a pandas data frame can be done as follows::

    import urllib2
    import json
    import pyjstat
    results = pyjstat.from_json_stat(json.load(urllib2.urlopen(
    'http://json-stat.org/samples/oecd-canada.json')))
    print results

"""

import json
from operator import itemgetter

import numpy
import pandas as pd
import numpy as np
from collections import OrderedDict
import abc
import requests
import logging
import inspect
import warnings


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder class for Numpy data types.

    """
    def default(self, obj):
        if (isinstance(obj, np.integer) or isinstance(obj, np.int64)):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)


def to_int(variable):
    """Convert variable to integer or string depending on the case.

    Args:
      variable (string): a string containing a real string or an integer.

    Returns:
      variable(int, string): an integer or a string, depending on the content\
                             of variable.

    """
    try:
        return int(variable)
    except ValueError:
        return variable


def to_str(variable):
    """Convert variable to integer or string depending on the case.

    Args:
      variable (string): a string containing a real string or an integer.

    Returns:
      variable(int, string): an integer or a string, depending on the content\
                             of variable.

    """
    try:
        int(variable)
        return str(variable)
    except ValueError:
        return variable


def check_version(dataset, version):
    """Checks json-stat version for a given dataset.

       Args:
         dataset (OrderedDict): data in JSON-stat format, previously \
                                   deserialized to a python object by \
                                   json.load() or json.loads(),

       Returns:
         (boolean): True of False.

       """

    if (float(dataset.get('version')) >= float(version)
        if dataset.get('version') else False):
        return True
    else:
        return False


def check_input(naming):
    """Check and validate input params.

    Args:
      naming (string): a string containing the naming type (label or id).

    Returns:
      Nothing

    Raises:
      ValueError: if the parameter is not in the allowed list.

    """

    if naming not in ['label', 'id']:
        raise ValueError('naming must be "label" or "id"')


def get_dimensions(js_dict, naming):
    """Get dimensions from input data.

    Args:
      js_dict (dict): dictionary containing dataset data and metadata.
      naming (string, optional): dimension naming. Possible values: 'label' \
                                 or 'id'.

    Returns:
      dimensions (list): list of pandas data frames with dimension \
                         category data.
      dim_names (list): list of strings with dimension names.
    """

    dimensions = []
    dim_names = []
    if (check_version(js_dict, '2.0')):
        dimension_dict = js_dict
    else:
        dimension_dict = js_dict['dimension']
    for dim in dimension_dict['id']:
        dim_name = js_dict['dimension'][dim]['label']
        if not dim_name:
            dim_name = dim
        if naming == 'label':
            dim_label = get_dim_label(js_dict, dim)
            dimensions.append(dim_label)
            dim_names.append(dim_name)
        else:
            dim_index = get_dim_index(js_dict, dim)
            dimensions.append(dim_index)
            dim_names.append(dim)
    return dimensions, dim_names


def get_dim_label(js_dict, dim):
    """Get label from a given dimension.

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
                              axis=1)
        dim_label.columns = ['id', 'label']
    else:
        dim_label = pd.DataFrame(list(zip(dim_label.keys(),
                                          dim_label.values())),
                                 index=dim_label.keys(),
                                 columns=['id', 'label'])
    # index must be added to dim label so that it can be sorted
    try:
        dim_index = js_dict['dimension'][dim]['category']['index']
    except KeyError:
        dim_index = pd.DataFrame(list(zip([dim_label['id'][0]], [0])),
                                 index=[0],
                                 columns=['id', 'index'])
    else:
        if type(dim_index) is list:
            dim_index = pd.DataFrame(list(zip(dim_index,
                                              range(0, len(dim_index)))),
                                     index=dim_index, columns=['id', 'index'])
        else:
            dim_index = pd.DataFrame(list(zip(dim_index.keys(),
                                              dim_index.values())),
                                     index=dim_index.keys(),
                                     columns=['id', 'index'])
    dim_label = pd.merge(dim_label, dim_index, on='id').sort_values(by='index')
    return dim_label


def get_dim_index(js_dict, dim):
    """Get index from a given dimension.

    Args:
      js_dict (dict): dictionary containing dataset data and metadata.
      dim (string): dimension name obtained from JSON file.

    Returns:
      dim_index (pandas.DataFrame): DataFrame with index-based dimension data.

    """

    try:
        dim_index = js_dict['dimension'][dim]['category']['index']
    except KeyError:
        dim_label = get_dim_label(js_dict, dim)
        dim_index = pd.DataFrame(list(zip([dim_label['id'][0]], [0])),
                                 index=[0],
                                 columns=['id', 'index'])
    else:
        if type(dim_index) is list:
            dim_index = pd.DataFrame(list(zip(dim_index,
                                              range(0, len(dim_index)))),
                                     index=dim_index, columns=['id', 'index'])
        else:
            dim_index = pd.DataFrame(list(zip(dim_index.keys(),
                                              dim_index.values())),
                                     index=dim_index.keys(),
                                     columns=['id', 'index'])
    dim_index = dim_index.sort_values(by='index')
    return dim_index


def get_values(js_dict, value='value'):
    """Get values from input data.

    Args:
      js_dict (dict): dictionary containing dataset data and metadata.
      value (string, optional): name of the value column. Defaults to 'value'.

    Returns:
      values (list): list of dataset values.

    """

    values = js_dict[value]
    if type(values) is list:
        if type(values[0]) is not dict or tuple:
            return values
    # being not a list of dicts or tuples leaves us with a dict...
    values = {int(key): value for (key, value) in values.items()}
    max_val = max(values.keys(), key=int) + 1
    vals = []
    for i in range(0, max_val):
        vals.append(values.get(i))
    values = vals
    return values


def get_df_row(dimensions, naming='label', i=0, record=None):
    """Generate row dimension values for a pandas dataframe.

    Args:
      dimensions (list): list of pandas dataframes with dimension labels \
                         generated by get_dim_label or get_dim_index methods.
      naming (string, optional): dimension naming. Possible values: 'label' \
                                 or 'id'.
      i (int): dimension list iteration index. Default is 0, it's used in the \
                         recursive calls to the method.
      record (list): list of values representing a pandas dataframe row, \
                     except for the value column. Default is empty, it's used \
                     in the recursive calls to the method.

    Yields:
      list: list with pandas dataframe column values except for value column

    """

    check_input(naming)
    if i == 0 or record is None:
        record = []
    for dimension in dimensions[i][naming]:
        record.append(dimension)
        if len(record) == len(dimensions):
            yield record

        if i + 1 < len(dimensions):
            for row in get_df_row(dimensions, naming, i + 1, record):
                yield row
        if len(record) == i + 1:
            record.pop()


def uniquify(seq):
    """Return unique values in a list in the original order. See:  \
        http://www.peterbe.com/plog/uniqifiers-benchmark

    Args:
      seq (list): original list.

    Returns:
      list: list without duplicates preserving original order.

    """

    seen = set()
    seen_add = seen.add
    return [x for x in seq if x not in seen and not seen_add(x)]


def generate_df(js_dict, naming, value="value"):
    """Decode JSON-stat dict into pandas.DataFrame object. Helper method \
       that should be called inside from_json_stat().

    Args:
      js_dict(OrderedDict): OrderedDict with data in JSON-stat format, \
                            previously deserialized into a python object by \
                            json.load() or json.loads(), for example.
      naming(string): dimension naming. Possible values: 'label' or 'id.'
      value (string, optional): name of the value column. Defaults to 'value'.

    Returns:
      output(DataFrame): pandas.DataFrame with converted data.

    """

    values = []

    dimensions, dim_names = get_dimensions(js_dict, naming)
    values = get_values(js_dict, value=value)

    output = pd.DataFrame([category + [values[i]]
                           for i, category in
                           enumerate(get_df_row(dimensions, naming))])
    output.columns = dim_names + [value]
    output.index=range(0, len(values))
    return output


def from_json_stat(datasets, naming='label', value='value'):
    """Decode JSON-stat formatted data into pandas.DataFrame object.

    Args:
      datasets(OrderedDict, list): data in JSON-stat format, previously \
                                   deserialized to a python object by \
                                   json.load() or json.loads(), for example.\
                                   Both List and OrderedDict are accepted \
                                   as inputs.
      naming(string, optional): dimension naming. Possible values: 'label'
                                or 'id'.Defaults to 'label'.
      value (string, optional): name of the value column. Defaults to 'value'.

    Returns:
      results(list): list of pandas.DataFrame with imported data.

    """

    check_input(naming)
    results = []
    if type(datasets) is list:
        for idx, element in enumerate(datasets):
            for dataset in element:
                js_dict = datasets[idx][dataset]
                results.append(generate_df(js_dict, naming, value))
    elif isinstance(datasets, OrderedDict) or type(datasets) is dict or isinstance(datasets,Dataset):
        if 'class' in datasets:
            if datasets['class'] == 'dataset':
                js_dict = datasets
                results.append(generate_df(js_dict, naming, value))
        else:  # 1.00 bundle type
            for dataset in datasets:
                js_dict = datasets[dataset]
                results.append(generate_df(js_dict, naming, value))
    return results


def to_json_stat(input_df, value='value', output='list', version='1.3'):
    """Encode pandas.DataFrame object into JSON-stat format. The DataFrames
       must have exactly one value column.

    Args:
      df(pandas.DataFrame): pandas data frame (or list of data frames) to
      encode.
      value (string, optional): name of the value column. Defaults to 'value'.
      output(string): accepts two values: 'list' or 'dict'. Produce list of\
                      dicts or dict of dicts as output.
      version(string): desired json-stat version. 2.0 is the default now.\
                       Apart from this, only older 1.3 format is accepted.

    Returns:
      output(string): String with JSON-stat object.

    """

    warnings.warn(
        "shouldn't use this function anymore! Now use XYZ.",
        DeprecationWarning
    )
    data = []
    if output == 'list':
        result = []
    elif output == 'dict':
        result = OrderedDict({})
    if isinstance(input_df, pd.DataFrame):
        data.append(input_df)
    else:
        data = input_df
    for row, dataframe in enumerate(data):
        pd.notnull(dataframe[value])
        dims = data[row].filter([item for item in data[row].columns.values
                                 if item not in value])
        if len(dims.columns.values) != len(set(dims.columns.values)):
            raise ValueError('Non-value columns must constitute a unique ID')
        dim_names = list(dims)
        categories = [{to_int(i):
                       {"label": to_str(i),
                        "category":
                            {"index":
                             OrderedDict([(to_str(j), to_int(k))
                                          for k, j in enumerate(
                                              uniquify(dims[i]))]),
                             "label":
                                 OrderedDict([(to_str(j), to_str(j))
                                              for k, j in enumerate(
                                                  uniquify(dims[i]))])}}}
                      for i in dims.columns.values]
        if (float(version) >= 2.0):

            dataset =  {"dimension": OrderedDict(),
                        value: [x for x in dataframe[value].values]}

            dataset["version"] = version
            dataset["class"] = "dataset"
            for category in categories:
                dataset["dimension"].update(category)
            dataset.update({"id": dim_names})
            dataset.update({"size": [len(dims[i].unique())
                                                for i in dims.columns.values]})
            for category in categories:
                dataset["dimension"].update(category)
        else:
            dataset = {"dataset" + str(row + 1):
                           {"dimension": OrderedDict(),
                            value: [x for x in dataframe[value].values]}}
            for category in categories:
                dataset["dataset" + str(row + 1)][
                    "dimension"].update(category)
            dataset["dataset" + str(row + 1)][
                "dimension"].update({"id": dim_names})
            dataset["dataset" + str(row + 1)][
                "dimension"].update({"size": [len(dims[i].unique())
                                              for i in dims.columns.values]})
            for category in categories:
                dataset["dataset" + str(row + 1)][
                    "dimension"].update(category)

        if output == 'list':
            result.append(dataset)
        elif output == 'dict':
            result.update(dataset)
        else:
            result = None
    return json.dumps(result, cls=NumpyEncoder)

def request(path):
    """Send a request to a given URL accepting JSON format and return a \
       deserialized Python object.

    Args:
      path (str): The URI to be requested.

    Returns:
      response: Deserialized JSON Python object.

    Raises:
      HTTPError: the HTTP error returned by the requested server.
      InvalidURL: an invalid URL has been requested.
      Exception: generic exception.

    """
    headers = {'Accept': 'application/json'}
    try:
            requested_object = requests.get(path, headers=headers)
            requested_object.raise_for_status()
    except requests.exceptions.HTTPError as exception:
        LOGGER.error((inspect.stack()[0][3]) + ': HTTPError = ' +
                     str(exception.response.status_code) + ' ' +
                     str(exception.response.reason) + ' ' + str(path))
        raise
    except requests.exceptions.InvalidURL as exception:
        LOGGER.error('URLError = ' + str(exception.reason) + ' ' + str(path))
        raise
    except Exception:
        import traceback
        LOGGER.error('Generic exception: ' + traceback.format_exc())
        raise
    else:
        response = requested_object.json()
        return response


class Dataset(OrderedDict):
    """Class mapping """

    @classmethod
    def read(cls, data):
        if (isinstance(data, pd.DataFrame)):
            return cls((json.loads(to_json_stat(data, output='dict', version='2.0'),object_pairs_hook=OrderedDict)))
        elif (isinstance(data, OrderedDict)):
            return cls(data)
        elif (data.startswith(("http://","https://"))):
            return cls(request(data))
        else:
            raise TypeError

    def write(self, output='jsonstat'):
        if (output == 'jsonstat'):
            return (json.dumps(self))
        elif (output == 'dataframe'):
            return from_json_stat(self)[0]
        else:
            raise ValueError("Allowed arguments are 'jsonstat' or 'dataframe'")


    def get_dimension_index(self, name, value):

        if (not ('index' in self.get('dimension', {}).get(name,{}).get('category', {}))):
            return 0;
        ndx = self['dimension'][name]['category']['index']

        if (isinstance(ndx, list)):
            return ndx.index(value)
        else:
            return ndx[value]

    def get_dimension_indices(self, query):
        ids = self['id'] if self.get('id') else self['dimension']['id']
        ndims = len(ids)
        indices = []

        for idx, id in enumerate(ids):
            indices.append(self.get_dimension_index(id, [d.get(id) for d in query if id in d][0]))

        return indices

    def get_value_index(self, indices):

        size = self['size'] if self.get('size') else self['dimension']['size']
        ndims = len(size)
        mult = 1;
        num = 0;
        for idx, dim in enumerate(size):
            mult *= size[ndims - idx] if (idx > 0) else 1
            num += mult * indices[ndims - idx - 1]
        return num

    def get_value_by_index(self, index):
        return self['value'][index]

    def get_value(self, query):
        indices = self.get_dimension_indices(query)
        index = self.get_value_index(indices)
        value = self.get_value_by_index(index)
        return value

class Collection(OrderedDict):
    """Class mapping """



    @classmethod
    def read(cls, data):
        if (isinstance(data, OrderedDict)):
            return cls(data)
        elif (data.startswith(("http://", "https://"))):
            return cls(request(data))
        else:
            raise TypeError

    def write(self,output='jsonstat'):
        """Convert Json-stat data into list of pandas.DataFrame objects.

            Returns:
            Python Pandas Dataframe.
        """
        if (output == 'jsonstat'):
            return (json.dumps(self))
        elif (output == 'dataframe_list'):
            df_list = []
            for item in self['link']['item']:
                if (item['class'] == 'dataset'):
                    df_list.append(Dataset.read(item['href']).write('dataframe'))
            return df_list
        else:
            raise ValueError("Allowed arguments are 'jsonstat' or 'dataframe_list'")

        #TODO collection with items of type collection?? recursive call

    def get(self, i):
        if (self['link']['item'][i]['class'] == 'dataset'):
            return Dataset.read(self['link']['item'][i]['href'])
        else:
            print ("handle error")



