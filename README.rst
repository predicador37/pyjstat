**LAST RELEASE 2.0**: update to 2.0 version is highly recommended, since it 
supports JSON-stat 2.0 and brings other improvements. Also, Version 2.X starts 
to **support Pandas 1.X, and won't have backwards compatibility**.
**WARNING**: support for Python 2.7 has been removed in pyjstat 2.0.

=======
pyjstat
=======

.. image:: https://travis-ci.org/predicador37/pyjstat.svg?branch=master
    :target: https://travis-ci.org/predicador37/pyjstat

**pyjstat** is a python library for **JSON-stat** formatted data manipulation
which allows reading and writing JSON-stat [1]_ format with python,using the
DataFrame structures provided by the widely accepted pandas library [2]_.
The JSON-stat format is a simple lightweight JSON format for data
dissemination, currently in its 2.0 version.
Pyjstat is inspired in rjstat [3]_, a library to read and write
JSON-stat with R, by ajschumacher. Note that, like in the rjstat project,
not all features are supported (i.e. not all metadata are converted).
**pyjstat** is provided under the Apache License 2.0.

.. [1] http://json-stat.org/ for JSON-stat information
.. [2] http://pandas.pydata.org for Python Data Analysis Library information
.. [3] https://github.com/ajschumacher/rjstat for rjstat library information

This library was first developed to work with Python 2.7. With some fixes
(thanks to @andrekittredge), now it works with Python 3.4 too.

Support for JSON-stat 1.3 and 2.0 is provided. JSON-stat 1.3 methods are
deprecated now and shouldn't be used in the future, but backwards compatibility
has been preserved.

Pyjstat 1.0 is aimed for simplicity. JSON-stat classes have been replicated
(Dataset, Collection and Dimension) and provided with simple read() and write()
methods. Funcionality covers common use cases as having a URL or dataframe
as data sources.

Methods for retrieving the value of a particular cube cell are taken from the
JSON-stat Javascript sample code. Thanks to @badosa for this.

Also, version 1.0 makes use of the requests package internally, which should
make downloading of datasets easier.

Test coverage is 88% and Travis CI is used.

Finally, note that the new classes and methods are inspired by JSON-stat 2.0,
and hence, won't work with previous versions of JSON-stat. However, older
methods are still available incorporating bug fixes and performance
improvements.

Installation
============

pyjstat requires pandas package. For installation::

    pip install pyjstat

Usage of version 1.0 and newer (with JSON-stat 2.0 support)
===========================================================

Dataset operations: read and write
----------------------------------

Typical usage often looks like this::

    from pyjstat import pyjstat

    EXAMPLE_URL = 'http://json-stat.org/samples/galicia.json'

    # read from json-stat
    dataset = pyjstat.Dataset.read(EXAMPLE_URL)

    # write to dataframe
    df = dataset.write('dataframe')
    print(df)

    # read from dataframe
    dataset_from_df = pyjstat.Dataset.read(df)

    # write to json-stat
    print(dataset_from_df.write())

Dataset operation: get_value
----------------------------------

This operation mimics the Javascript example in the JSON-stat web page::

    from pyjstat import pyjstat

    EXAMPLE_URL = 'http://json-stat.org/samples/oecd.json'
    query = [{'concept': 'UNR'}, {'area': 'US'}, {'year': '2010'}]

    dataset = pyjstat.Dataset.read(EXAMPLE_URL)
    print(dataset.get_value(query))

Collection operations: read and write
-------------------------------------

A collection can be parsed into a list of dataframes::

    from pyjstat import pyjstat

    EXAMPLE_URL = 'http://json-stat.org/samples/collection.json'

    collection = pyjstat.Collection.read(EXAMPLE_URL)
    df_list = collection.write('dataframe_list')
    print(df_list)

Example with UK ONS API
-----------------------

In the following example, apikey parameter must be replaced by a real api key
from ONS. This dataset corresponds to residence type by sex by age in London::

    EXAMPLE_URL = 'http://web.ons.gov.uk/ons/api/data/dataset/DC1104EW.json?'\
                  'context=Census&jsontype=json-stat&apikey=yourapikey&'\
                  'geog=2011HTWARDH&diff=&totals=false&'\
                  'dm/2011HTWARDH=E12000007'
    dataset = pyjstat.Dataset.read(EXAMPLE_URL)
    df = dataset.write('dataframe')
    print(df)

More examples
-------------

More examples can be found in the examples directory, both for versions 1.3
and 2.0.


Usage of version 0.3.5 and older (with support for JSON-stat 1.3)
=================================================================

This syntax is deprecated and therefore not recommended anymore.

From JSON-stat to pandas DataFrame
-----------------------------------

Typical usage often looks like this::

    from pyjstat import pyjstat
    import requests
    from collections import OrderedDict

    EXAMPLE_URL = 'http://json-stat.org/samples/us-labor.json'

    data = requests.get(EXAMPLE_URL)
    results = pyjstat.from_json_stat(data.json(object_pairs_hook=OrderedDict))
    print (results)

From pandas DataFrame to JSON-stat
----------------------------------

The same data can be converted into JSON-stat, with some unavoidable metadata
loss::

    from pyjstat import pyjstat
    import requests
    from collections import OrderedDict
    import json

    EXAMPLE_URL = 'http://json-stat.org/samples/us-labor.json'

    data = requests.get(EXAMPLE_URL)
    results = pyjstat.from_json_stat(data.json(object_pairs_hook=OrderedDict))
    print (results)
    print (json.dumps(json.loads(pyjstat.to_json_stat(results))))

Changes
-------

For a changes, fixes, improvements and new features reference, see CHANGES.txt.
