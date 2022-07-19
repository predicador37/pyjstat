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

import inspect
import json
import logging
import warnings
from collections import OrderedDict
from datetime import datetime

import numpy as np

import pandas as pd

import requests

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

try:
    basestring
except NameError:
    basestring = str


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder class for Numpy data types."""

    def default(self, obj):
        """Encode by default."""
        if isinstance(obj, np.integer) or isinstance(obj, np.int64):
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
      variable(int, string): an integer or a string, depending on the content
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
      variable(int, string): an integer or a string, depending on the content
                             of variable.

    """
    try:
        int(variable)
        return str(variable)
    except ValueError:
        return variable


def check_version_2(dataset):
    """Check for json-stat version.

    Check if json-stat version attribute exists and is equal or greater
    than 2.0 for a given dataset.

    Args:
        dataset (OrderedDict): data in JSON-stat format, previously
                                   deserialized to a python object by
                                   json.load() or json.loads(),

    Returns:
        bool: True if version exists and is equal or greater than 2.0,
               False otherwise. For datasets without the version attribute,
               always return False.

    """
    if float(dataset.get('version')) >= 2.0 \
            if dataset.get('version') else False:
        if 'id' not in dataset:
            # Some datasets claim to be 2.0, but don't have version 2 structure.
            return False
        return True
    else:
        return False


def unnest_collection(collection, df_list):
    """Unnest collection extracting its datasets and converting them to df.

    Args:
        collection (OrderedDict): data in JSON-stat format, previously
                                  deserialized to a python object by
                                  json.load() or json.loads(),
        df_list (list): list variable which will contain the converted
                        datasets.

    Returns:
        Nothing.

    """
    for item in collection['link']['item']:
        if item['class'] == 'dataset':
            df_list.append(Dataset.read(item['href']).write('dataframe'))
        elif item['class'] == 'collection':
            nested_collection = request(item['href'])
            unnest_collection(nested_collection, df_list)


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
      naming (string, optional): dimension naming. Possible values: 'label'
                                 or 'id'.

    Returns:
      dimensions (list): list of pandas data frames with dimension
                         category data.
      dim_names (list): list of strings with dimension names.

    """
    dimensions = []
    dim_names = []
    if check_version_2(js_dict):
        dimension_dict = js_dict
    else:
        dimension_dict = js_dict['dimension']
    for dim in dimension_dict['id']:
        if 'label' in js_dict['dimension'][dim]:
            dim_name = js_dict['dimension'][dim]['label']
        else:
            # All datasets don't have labels for dimensions
            dim_name = dim
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


def get_dim_label(js_dict, dim, dim_input="dataset"):
    """Get label from a given dimension.

    Args:
      js_dict (dict): dictionary containing dataset data and metadata.
      dim (string): dimension name obtained from JSON file.

    Returns:
      dim_label(pandas.DataFrame): DataFrame with label-based dimension data.

    """
    if dim_input == 'dataset':
        dim_input = js_dict['dimension'][dim]
        label_col = 'label'
    elif dim_input == 'dimension':
        label_col = js_dict['label']
        dim_input = js_dict
    else:
        raise ValueError

    try:
        dim_label = dim_input['category']['label']

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
                                 columns=['id', label_col])
    # index must be added to dim label so that it can be sorted
    try:
        dim_index = dim_input['category']['index']
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

    if js_dict.get('size'):
        max_val = np.prod(np.array((js_dict['size'])))
    else:
        max_val = np.prod(np.array((js_dict['dimension']['size'])))
    vals = max_val * [None]
    for (key, value) in values.items():
        vals[key] = value

    values = vals
    return values


def get_df_row(dimensions, naming='label', i=0, record=None):
    """Generate row dimension values for a pandas dataframe.

    Args:
      dimensions (list): list of pandas dataframes with dimension labels
                         generated by get_dim_label or get_dim_index methods.
      naming (string, optional): dimension naming. Possible values: 'label'
                                 or 'id'.
      i (int): dimension list iteration index. Default is 0, it's used in the
                         recursive calls to the method.
      record (list): list of values representing a pandas dataframe row,
                     except for the value column. Default is empty, it's used
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
    """Return unique values in a list in the original order.

    See: http://www.peterbe.com/plog/uniqifiers-benchmark

    Args:
      seq (list): original list.

    Returns:
      list: list without duplicates preserving original order.

    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if x not in seen and not seen_add(x)]


def generate_df(js_dict, naming, value="value"):
    """Decode JSON-stat dict into pandas.DataFrame object.

    Helper method that should be called inside from_json_stat().

    Args:
      js_dict(OrderedDict): OrderedDict with data in JSON-stat format,
                            previously deserialized into a python object by
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
    output.index = range(0, len(values))
    return output


def from_json_stat(datasets, naming='label', value='value'):
    """Decode JSON-stat formatted data into pandas.DataFrame object.

    Args:
      datasets(OrderedDict, list): data in JSON-stat format, previously
                                   deserialized to a python object by
                                   json.load() or json.loads(), for example.
                                   Both List and OrderedDict are accepted
                                   as inputs.
      naming(string, optional): dimension naming. Possible values: 'label'
                                or 'id'.Defaults to 'label'.
      value (string, optional): name of the value column. Defaults to 'value'.

    Returns:
      results(list): list of pandas.DataFrame with imported data.

    """
    warnings.warn(
        "Shouldn't use this function anymore! Now use read() methods of"
        "Dataset, Collection or Dimension.",
        DeprecationWarning
    )

    check_input(naming)
    results = []
    if type(datasets) is list:
        for idx, element in enumerate(datasets):
            for dataset in element:
                js_dict = datasets[idx][dataset]
                results.append(generate_df(js_dict, naming, value))
    elif isinstance(datasets, OrderedDict) or type(datasets) is dict or \
            isinstance(datasets, Dataset):
        if 'class' in datasets:
            if datasets['class'] == 'dataset':
                js_dict = datasets
                results.append(generate_df(js_dict, naming, value))
        else:  # 1.00 bundle type
            for dataset in datasets:
                js_dict = datasets[dataset]
                results.append(generate_df(js_dict, naming, value))
    return results


def _round_decimals(dataframe, units, roles, value):
    """Round values according to units definition."""
    if not isinstance(dataframe, pd.DataFrame):
        return dataframe
    if not isinstance(units, dict):
        return dataframe
    if not isinstance(roles, dict):
        return dataframe
    if not isinstance(value, str):
        return dataframe

    df = dataframe.copy(deep=True)
    for unit in units.keys():
        if unit in roles['metric']:
            if '*' in units[unit].keys():
                decimals = units[unit]['*'].get('decimals')
                if decimals is not None:
                    df[value] = df[value].round(decimals)
            else:
                for label in units[unit].keys():
                    decimals = units[unit][label].get('decimals')
                    if decimals is not None:
                        for idx, row in df.iterrows():
                            if row[unit] == label:
                                df.at[
                                    idx, value] = df.at[
                                        idx, value].round(decimals)

    return df


def _add_units_to_categories(categories, units, roles):
    """Add units to categories according to units definition."""
    if not isinstance(categories, list):
        return categories
    if not isinstance(units, dict):
        return categories
    if not isinstance(roles, dict):
        return categories

    for unit in units.keys():
        if unit in roles['metric']:
            for idx, category in enumerate(categories):
                if unit == list(category)[0]:
                    if '*' in units[unit].keys():
                        units_updated = {}
                        for c in categories[idx][unit]['category']['label']:
                            units_updated.update(
                                {c: {
                                    'label': units[
                                        unit]['*'].get('label'),
                                    'decimals': units[
                                        unit]['*'].get('decimals')
                                }}
                            )
                        categories[idx][unit]['category'].update(
                            {"unit": units_updated})
                    else:
                        categories[idx][unit]['category'].update(
                            {"unit": units[unit]})

    return categories


def _get_categories(data, unit=None, role=None, value='value'):
    """Return a list of categories according to dimensions.

    When unit, role and value are included in parameters,
    decimals are rounded, also adds units dictionary to result.

    Args:
      data(pandas.Dataframe): must have exactly one value column.
      value (string, optional): name of the value column. Defaults to 'value'.
      role(dict, optional): roles for dimensions.
      unit(dict, optional): unit for variables, if there is only one
                            element named '*' it will repeated for all.
    """
    dims = data.filter([item for item in data.columns.values
                        if item not in value])
    if isinstance(unit, dict) and isinstance(role, dict):
        data = _round_decimals(data, unit, role, value)
        categories_without_units = [
            {to_int(i):
                {"label": to_str(i),
                 "category":
                 {"index":
                  OrderedDict([(to_str(j), to_int(k))
                              for k, j in
                              enumerate(uniquify(dims[i]))]),
                  "label":
                  OrderedDict([(to_str(j), to_str(j))
                              for k, j in
                              enumerate(uniquify(dims[i]))])
                  }}}
            for i in dims.columns.values]
        categories = _add_units_to_categories(
            categories_without_units, unit, role)
    else:
        categories = [{to_int(i):
                       {"label": to_str(i),
                        "category":
                        {"index":
                         OrderedDict([(to_str(j), to_int(k))
                                      for k, j in
                                      enumerate(uniquify(dims[i]))]),
                         "label":
                         OrderedDict([(to_str(j), to_str(j))
                                      for k, j in
                                      enumerate(uniquify(dims[i]))])}}}
                      for i in dims.columns.values]

    return categories


def to_json_stat(input_df, value='value',
                 output='list', version='1.3',
                 updated=datetime.today(), source='Self-elaboration',
                 note=None, role=None, unit=None):
    """Encode pandas.DataFrame object into JSON-stat format.

    The DataFrames must have exactly one value column.

    Args:
      df(pandas.DataFrame): pandas data frame (or list of data frames) to
      encode.
      value (string, optional): name of the value column. Defaults to 'value'.
      output(string): accepts two values: 'list' or 'dict'. Produce list of
                      dicts or dict of dicts as output.
      version(string): desired json-stat version. 2.0 is preferred now.
                       Apart from this, only older 1.3 format is accepted,
                       which is the default parameter in order to preserve
                       backwards compatibility.
      updated(datetime): updated metadata in JSON-stat standard. Must be a
                         datetime in ISO format.
      source(string, optional): data source in JSON-stat standard.
      note(string, optional): information for metadata.
      role(dict, optional): roles for dimensions.
      unit(dict, optional): unit for variables, if there is only one
                             element named '*' it will repeated for all.

    Returns:
      output(string): String with JSON-stat object.

    """
    warnings.warn(
        "Shouldn't use this function anymore! Now use write() methods of"
        "Dataset, Collection or Dimension.",
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
        dims = data[row].filter([item for item in data[row].columns.values
                                 if item not in value])
        if len(dims.columns.values) != len(set(dims.columns.values)):
            raise ValueError('Non-value columns must constitute a unique ID')
        dim_names = list(dims)

        if isinstance(role, dict):
            for metric in role.get('metric'):
                uniques_dimensions = dataframe[metric].unique()
                for dimension in uniques_dimensions:
                    tmp_df = dataframe.query(metric+" == '"+dimension+"'")
                    time_column = tmp_df.loc[:, role.get('time')[0]]
                    if time_column.duplicated().any():
                        warnings.warn(
                            "Data duplicated in time dimension."
                            "Doesn't exist unique values for each dimension. ",
                            UserWarning
                        )

        categories = _get_categories(dataframe, unit, role, value)
        if float(version) >= 2.0:

            dataset = {"dimension": OrderedDict(),
                       value: [None if pd.isnull(x) else x
                               for x in dataframe[value].values]}

            dataset["version"] = version
            dataset["class"] = "dataset"
            dataset["updated"] = updated.isoformat()
            dataset["source"] = source
            if isinstance(role, dict):
                dataset["role"] = role
            if isinstance(note, str):
                dataset["note"] = [note]
            for category in categories:
                dataset["dimension"].update(category)
            dataset.update({"id": dim_names})
            dataset.update({"size": [len(dims[i].unique())
                                     for i in dims.columns.values]})
            for category in categories:
                dataset["dimension"].update(category)
        else:
            dataset = {"dataset" +
                       str(row + 1):
                       {"dimension": OrderedDict(),
                        value: [None if pd.isnull(x) else x
                                for x in dataframe[value].values]}}
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


def request(path, verify=True):
    """Send a request to a given URL accepting JSON format.

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
        requested_object = requests.get(path, headers=headers, verify=verify)
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
    """A class representing a JSONstat dataset."""

    def __init__(self, *args, **kwargs):
        """Initialize object."""
        super(Dataset, self).__init__(*args, **kwargs)

    @ classmethod
    def read(cls, data, verify=True, **kwargs):
        """Read data from URL, Dataframe, JSON string/file or OrderedDict.

        Args:
            data: can be a Pandas Dataframe, a JSON file, a JSON string,
                  an OrderedDict or a URL pointing to a JSONstat file.
            verify: whether to host's SSL certificate.
            kwargs: optional arguments for to_json_stat().
        Returns:
            An object of class Dataset populated with data.

        """
        if isinstance(data, pd.DataFrame):
            return cls((json.loads(
                to_json_stat(data, output='dict', version='2.0', **kwargs),
                object_pairs_hook=OrderedDict)))
        elif isinstance(data, OrderedDict):
            return cls(data)
        elif (isinstance(data, basestring)
              and data.startswith(("http://", "https://",
                                   "ftp://", "ftps://"))):
            # requests will do the rest...
            return cls(request(data, verify=verify))
        elif isinstance(data, basestring):
            try:
                json_dict = json.loads(data, object_pairs_hook=OrderedDict)
                return cls(json_dict)
            except ValueError:
                raise
        else:
            try:
                json_dict = json.load(data, object_pairs_hook=OrderedDict)
                return cls(json_dict)
            except ValueError:
                raise

    def write(self, output='jsonstat', naming="label", value='value'):
        """Write data from a Dataset object to JSONstat or Pandas Dataframe.

        Args:
            output(string): can accept 'jsonstat' or 'dataframe'. Default to
                            'jsonstat'.
            naming (string): optional, ingored if output = 'jsonstat'.
                             Dimension naming.
                Possible values: 'label' or 'id'. Defaults to 'label'.
            value (string): optional, ignored if output = 'jsonstat'.
                            Name of value column.
                Defaults to 'value'.

        Returns:
            Serialized JSONstat or a Pandas Dataframe,depending on the
            'output' parameter.

        """
        if output == 'jsonstat':
            return json.dumps(OrderedDict(self), cls=NumpyEncoder)
        elif output == 'dataframe':
            return from_json_stat(self, naming=naming, value=value)[0]
        else:
            raise ValueError("Allowed arguments are 'jsonstat' or 'dataframe'")

    def get_dimension_index(self, name, value):
        """Get a dimension index from its name.

        Convert a dimension ID string and a category ID string into the
        numeric index of that category in that dimension

        Args:
           name(string): ID string of the dimension.
           value(string): ID string of the category.

        Returns:
           ndx[value](int): index of the category in the dimension.

        """
        if 'index' not in self.get('dimension', {}). \
                get(name, {}).get('category', {}):
            return 0
        ndx = self['dimension'][name]['category']['index']

        if isinstance(ndx, list):
            return ndx.index(value)
        else:
            return ndx[value]

    def get_dimension_indices(self, query):
        """Get dimension indices.

        Converts a dimension/category list of dicts into a list of
        dimension indices.

        Args:
           query(list): dimension/category list of dicts.

        Returns:
           indices(list): list of dimensions' indices.

        """
        ids = self['id'] if self.get('id') else self['dimension']['id']
        indices = []

        for idx, ident in enumerate(ids):
            indices.append(self.get_dimension_index(
                ident, [d.get(ident) for d in query if ident in d][0]))

        return indices

    def get_value_index(self, indices):
        """Convert a list of dimension indices into a numeric value index.

        Args:
            indices(list): list of dimension's indices.

        Returns:
           num(int): numeric value index.

        """
        size = self['size'] if self.get('size') else self['dimension']['size']
        ndims = len(size)
        mult = 1
        num = 0
        for idx, dim in enumerate(size):
            mult *= size[ndims - idx] if (idx > 0) else 1
            num += mult * indices[ndims - idx - 1]
        return num

    def get_value_by_index(self, index):
        """Convert a numeric value index into its data value.

        Args:
            index(int): numeric value index.

        Returns:
            self['value'][index](float): Numeric data value.

        """
        return self['value'][index]

    def get_value(self, query):
        """Get data value.

        Convert a dimension/category list of dicts into a data value
        in three steps.

        Args:
           query(list): list of dicts with the desired query.

        Returns:
           value(float): numeric data value.

        """
        indices = self.get_dimension_indices(query)
        index = self.get_value_index(indices)
        value = self.get_value_by_index(index)
        return value


class Dimension(OrderedDict):
    """A class representing a JSONstat dimension."""

    def __init__(self, *args, **kwargs):
        """Initialize object."""
        super(Dimension, self).__init__(*args, **kwargs)

    @ classmethod
    def read(cls, data):
        """Read data from URL, Dataframe, JSON string/file or OrderedDict.

        Args:
            data: can be a Pandas Dataframe, a JSON string, a JSON file,
                  an OrderedDict or a URL pointing to a JSONstat file.

        Returns:
            An object of class Dimension populated with data.

        """
        if isinstance(data, pd.DataFrame):
            output = OrderedDict({})
            output['version'] = '2.0'
            output['class'] = 'dimension'
            [label] = [x for x in list(data.columns.values) if
                       x not in ['id', 'index']]
            output['label'] = label
            output['category'] = OrderedDict({})
            output['category']['index'] = data.id.tolist()
            output['category']['label'] = OrderedDict(
                zip(data.id.values, data[label].values))
            return cls(output)
        elif isinstance(data, OrderedDict):
            return cls(data)
        elif isinstance(data, basestring) and data.startswith(("http://",
                                                               "https://",
                                                               "ftp://",
                                                               "ftps://")):
            return cls(request(data))
        elif isinstance(data, basestring):
            try:
                json_dict = json.loads(data, object_pairs_hook=OrderedDict)
                return cls(json_dict)
            except ValueError:
                raise
        else:
            try:
                json_dict = json.load(data, object_pairs_hook=OrderedDict)
                return cls(json_dict)
            except ValueError:
                raise

    def write(self, output='jsonstat'):
        """Write data from a Dataset object to JSONstat or Pandas Dataframe.

        Args:
            output(string): can accept 'jsonstat' or 'dataframe'

        Returns:
            Serialized JSONstat or a Pandas Dataframe,depending on the
            'output' parameter.

        """
        if output == 'jsonstat':
            return json.dumps(OrderedDict(self), cls=NumpyEncoder)
        elif output == 'dataframe':
            return get_dim_label(self, self['label'], 'dimension')
        else:
            raise ValueError("Allowed arguments are 'jsonstat' or 'dataframe'")


class Collection(OrderedDict):
    """A class representing a JSONstat collection."""

    def __init__(self, *args, **kwargs):
        """Initialize object."""
        super(Collection, self).__init__(*args, **kwargs)

    @ classmethod
    def read(cls, data):
        """Read data from URL or OrderedDict.

        Args:
            data: can be a URL pointing to a JSONstat file, a JSON string
                  or an OrderedDict.

        Returns:
            An object of class Collection populated with data.

        """
        if isinstance(data, OrderedDict):
            return cls(data)
        elif isinstance(data, basestring) and data.startswith(("http://",
                                                               "https://",
                                                               "ftp://",
                                                               "ftps://")):
            return cls(request(data))
        elif isinstance(data, basestring):
            try:
                json_dict = json.loads(data, object_pairs_hook=OrderedDict)
                return cls(json_dict)
            except ValueError:
                raise
        else:
            try:
                json_dict = json.load(data, object_pairs_hook=OrderedDict)
                return cls(json_dict)
            except ValueError:
                raise

    def write(self, output='jsonstat'):
        """Write to JSON-stat or list of df.

        Writes data from a Collection object to JSONstat or list of Pandas
        Dataframes.

        Args:
            output(string): can accept 'jsonstat' or 'dataframe_list'

        Returns:
            Serialized JSONstat or a list of Pandas Dataframes,depending on
            the 'output' parameter.

        """
        if output == 'jsonstat':
            return json.dumps(self)
        elif output == 'dataframe_list':
            df_list = []
            unnest_collection(self, df_list)
            return df_list
        else:
            raise ValueError(
                "Allowed arguments are 'jsonstat' or 'dataframe_list'")

    def get(self, element):
        """Get element from collection.

        Get ith element from a collection in an object of the corresponding
        class.

        Args:
            output(string): can accept 'jsonstat' or 'dataframe_list'

        Returns:
            Serialized JSONstat or a list of Pandas Dataframes,depending on
            the 'output' parameter.

        """
        if self['link']['item'][element]['class'] == 'dataset':
            return Dataset.read(self['link']['item'][element]['href'])
        elif self['link']['item'][element]['class'] == 'collection':
            return Collection.read(self['link']['item'][element]['href'])
        elif self['link']['item'][element]['class'] == 'dimension':
            return Dimension.read(self['link']['item'][element]['href'])
        else:
            raise ValueError(
                "Class not allowed. Please use dataset, collection or "
                "dimension'")
