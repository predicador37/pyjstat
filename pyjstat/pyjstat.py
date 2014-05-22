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
import pandas as pd
from collections import OrderedDict


def check_input(naming):
    """Check and validate input params.

    Args:
      naming (string): a string containing the naming type (label or index)

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
      naming (string): a string containing the naming type (label or index).

    Returns:
      dimensions (list): list of pandas data frames with dimension \
                         category data.
      dim_names (list): list of strings with dimension names.
    """

    dimensions = []
    dim_names = []
    for dim in js_dict['dimension']['id']:
        dim_name = js_dict['dimension'][dim]['label']
        if not dim_name:
            dim_name = dim
        if (naming == 'label'):
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
        dim_label = pd.DataFrame(zip(dim_label.keys(),
                                     dim_label.values()),
                                 index=dim_label.keys(),
                                 columns=['id', 'label'])
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
        dim_index = pd.DataFrame(zip([dim_label['id'][0]], [0]),
                                 index=[0],
                                 columns=['id', 'index'])
    else:
        if type(dim_index) is list:
            dim_index = pd.DataFrame(zip(dim_index,
                                         range(0, len(dim_index))),
                                     index=dim_index,
                                     columns=['id', 'index'])
        else:
            dim_index = pd.DataFrame(zip(dim_index.keys(),
                                         dim_index.values()),
                                     index=dim_index.keys(),
                                     columns=['id', 'index'])
    return dim_index


def get_values(js_dict):
    """Get values from input data.

    Args:
      js_dict (dict): dictionary containing dataset data and metadata.

    Returns:
      values (list): list of dataset values.

    """

    values = js_dict['value']
    if type(values) is dict:  # see json-stat docs
        max_val = max(values.keys(), key=int)
        vals = []
        for element in values:
            for i in range(0, max_val):
                if element.key == i:
                    vals.append(element.value)
                else:
                    vals.append(None)
        values = vals
    return values


def get_df_row(dimensions, i=0, record=None):
    """Generate row dimension values for a pandas dataframe.

    Args:
      dimensions (list): list of pandas dataframes with dimension labels \
                         generated by get_dim_label or get_dim_index methods
      i (int, optional): dimension list iteration index. Default is 0, it's
                         used in the recursive calls to the method.
      record (list): list of values representing a pandas dataframe row, \
                     except for the value column. Default is empty, it's used \
                     in the recursive calls to the method.

    Yields:
      list: list with pandas dataframe column values except for value column

    """

    if (i == 0 or record is None):
        record = []
    for dimension in dimensions[i]['label']:
        record.append(dimension)
        if len(record) == len(dimensions):
            yield record

        if i + 1 < len(dimensions):
            for row in get_df_row(dimensions, i + 1, record):
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


def from_json_stat(datasets, naming='label'):
    """Decode JSON-stat format into pandas.DataFrame object

    Args:
      data(string): data in JSON-stat format to decode.
      naming(string): dimension naming. Possible values: 'label' or 'index'

    Returns:
      output(list): list of pandas.DataFrame with imported data.

    """

    check_input(naming)
    results = []
    for dataset in datasets:
        dimensions = []
        dim_names = []
        values = []
        js_dict = datasets[dataset]
        dimensions, dim_names = get_dimensions(js_dict, naming)
        values = get_values(js_dict)
        output = pd.DataFrame(columns=dim_names + [unicode('value', 'utf-8')],
                              index=range(0, len(values)))
        for i, category in enumerate(get_df_row(dimensions)):
            output.loc[i] = category + [values.pop(0)]
        output = output.convert_objects(convert_numeric=True)
        results.append(output)
    return(results)


def to_json_stat(input_df, value="value"):
    """Encode pandas.DataFrame object into JSON-stat format. The DataFrames
       must have exactly one value column.

    Args:
      df(pandas.DataFrame): pandas data frame (or list of data frames) to
      encode.
      value(string): name of value column.

    Returns:
      output(string): String with JSON-stat object.

    """

    data = []
    if isinstance(input_df, pd.DataFrame):
        data.append(input_df)
    else:
        data = input_df
    result = []
    for row, dataframe in enumerate(data):
        dims = data[row].filter([item for item in data[row].columns.values
                                 if item not in value])
        if len(dims.columns.values) != len(set(dims.columns.values)):
            raise ValueError('Non-value columns must constitute a unique ID')
        dim_names = list(dims)
        categories = [{i: {"label": i, "category": {"index":
                      OrderedDict([(str(j), str(k)) for k, j in
                           enumerate(uniquify(dims[i]))]),
                      "label":OrderedDict([(str(k), str(j)) for k, j in
                                          enumerate(uniquify(dims[i]))])}}}
                      for i in dims.columns.values]
        dataset = {"dataset" + str(row + 1): {"dimension": OrderedDict(),
                   "value": list(
                   dataframe['value'].where(
                       pd.notnull(dataframe['value']), None))}}
        for category in categories:
            dataset["dataset" + str(row + 1)]["dimension"].update(category)
        dataset[
            "dataset" + str(row + 1)]["dimension"].update({"id": dim_names})
        dataset["dataset" + str(row + 1)]["dimension"].update(
            {"size": [len(dims[i].unique()) for i in dims.columns.values]})
        for category in categories:
            dataset["dataset" + str(row + 1)]["dimension"].update(category)
        result.append(dataset)
    return json.dumps(result)
