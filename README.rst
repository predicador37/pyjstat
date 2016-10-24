**IMPORTANT NOTE**: update to 0.3.5 version is highly recommended, since previous versions contain an important bug related to dimension sorting and missing values. My apologies for any inconveniences.

=======
pyjstat
=======

.. image:: https://travis-ci.org/predicador37/pyjstat.svg?branch=master
    :target: https://travis-ci.org/predicador37/pyjstat

**pyjstat** is a python library for **JSON-stat** formatted data manipulation
which allows reading and writing JSON-stat [1]_ format with python,using the
DataFrame structures provided by the widely accepted pandas library [2]_.
The JSON-stat format is a simple lightweight JSON format for data
dissemination. Pyjstat is inspired in rjstat [3]_, a library to read and write
JSON-stat with R, by ajschumacher. Note that, like in the rjstat project,
not all features are supported (i.e. not all metadata are converted).
**pyjstat** is provided under the Apache License 2.0.

.. [1] http://json-stat.org/ for JSON-stat information
.. [2] http://pandas.pydata.org for Python Data Analysis Library information
.. [3] https://github.com/ajschumacher/rjstat for rjstat library information

This library was first developed to work with Python 2.7. With some fixes
(thanks to @andrekittredge), now it works with Python 3.4 too.

Installation
============

pyjstat requires pandas package. For installation::

    pip install pyjstat

Usage
=====

From JSON-stat to pandas DataFrame
-----------------------------------

Typical usage often looks like this::

    from pyjstat import pyjstat
    import requests
    from collections import OrderedDict

    EXAMPLE_URL = 'http://json-stat.org/samples/us-labor-ds.json'

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

    EXAMPLE_URL = 'http://json-stat.org/samples/us-labor-ds.json'

    data = requests.get(EXAMPLE_URL)
    results = pyjstat.from_json_stat(data.json(object_pairs_hook=OrderedDict))
    print (results)
    print (json.dumps(json.loads(pyjstat.to_json_stat(results))))

Changes
-------

For a changes, fixes, improvements and new features reference, see CHANGES.txt.
