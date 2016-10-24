# -*- coding: utf-8 -*-
"""
Unit tests for pyjstat

"""

from pyjstat import pyjstat
import unittest
import json
import os
from collections import OrderedDict


class TestPyjstat(unittest.TestCase):
    """ Unit tests for pyjstat """

    def setUp(self):
        """ Test data extracted from json-stat.org site """

        with open(os.path.join(os.path.dirname(__file__),
                               './data/oecd-canada.json')) as data_file:
            self.oecd_datasets = json.load(data_file,
                                           object_pairs_hook=OrderedDict)
        with open(os.path.join(os.path.dirname(__file__),
                               './data/ons.json')) as data_file:
            self.ons_datasets = json.load(data_file,
                                          object_pairs_hook=OrderedDict)
        with open(os.path.join(os.path.dirname(__file__),
                               './data/galicia-ds.json')) as data_file:
            self.galicia_dataset = json.load(data_file,
                                             object_pairs_hook=OrderedDict)
        with open(os.path.join(os.path.dirname(__file__),
                               './data/QS104EW.json')) as data_file:
            self.uk_dataset = json.load(data_file,
                                        object_pairs_hook=OrderedDict)
        with open(os.path.join(os.path.dirname(__file__),
                               './data/sample_data.json')) as data_file:
            self.sample_dataset = json.load(data_file,
                                            object_pairs_hook=OrderedDict)
        with open(os.path.join(os.path.dirname(__file__),
                               './data/us-labor-ds.json')) as data_file:
            self.uslabor_dataset = json.load(data_file,
                                             object_pairs_hook=OrderedDict)
        with open(os.path.join(os.path.dirname(__file__),
                               './data/statswe.json')) as data_file:
            self.sweden_dataset = json.load(data_file,
                                            object_pairs_hook=OrderedDict)
        with open(os.path.join(os.path.dirname(__file__),
                               './data/A02Level.json')) as data_file:
            self.ons_dataset = json.load(data_file,
                                         object_pairs_hook=OrderedDict)
        with open(os.path.join(os.path.dirname(__file__),
                               './data/CPI15.json')) as data_file:
            self.ons_cpi_dataset = json.load(data_file,
                                             object_pairs_hook=OrderedDict)

    def test_to_int(self):
        """ Test pyjstat to_int() """
        self.assertTrue(type(pyjstat.to_int("5") is int))
        self.assertTrue(type(pyjstat.to_int("label") is str))
        # not an integer...
        self.assertTrue(type(pyjstat.to_int("5.4") is str))

    def test_check_input(self):
        """ Test pyjstat check_input() """

        self.assertRaises(ValueError, pyjstat.check_input, 'name')
        self.assertTrue(pyjstat.check_input('label') is None)
        self.assertTrue(pyjstat.check_input('id') is None)

    def test_get_dim_index_with_index(self):
        """ Test pyjstat get_dim_index() using id as parameter """

        dim = self.oecd_datasets['oecd']['dimension']['id'][2]
        dims_df = pyjstat.get_dim_index(self.oecd_datasets['oecd'], dim)
        self.assertTrue(dims_df.iloc[0]['id'] == '2003')
        self.assertTrue(dims_df.iloc[-1]['index'] == 11)

    def test_get_dim_index_with_label(self):
        """ Test pyjstat get_dim_index() using label as parameter """

        dim = self.oecd_datasets['oecd']['dimension']['id'][0]
        dims_df = pyjstat.get_dim_index(self.oecd_datasets['oecd'], dim)
        self.assertTrue(dims_df.iloc[0]['id'] == 'UNR')
        self.assertTrue(dims_df.iloc[-1]['index'] == 0)

    def test_get_dim_label_with_label(self):
        """ Test pyjstat get_dim_label() using label as parameter """

        dim = self.oecd_datasets['oecd']['dimension']['id'][0]
        dims_df = pyjstat.get_dim_label(self.oecd_datasets['oecd'], dim)
        self.assertTrue(dims_df.iloc[0]['id'] == 'UNR')
        self.assertTrue(dims_df.iloc[-1]['label'] == 'unemployment rate')

    def test_get_dim_label_with_index(self):
        """ Test pyjstat get_dim_label() using id as parameter """

        dim = self.oecd_datasets['oecd']['dimension']['id'][2]
        dims_df = pyjstat.get_dim_label(self.oecd_datasets['oecd'], dim)
        self.assertTrue(dims_df.iloc[0]['id'] == '2003')
        self.assertTrue(dims_df.iloc[-1]['label'] == '2014')

    def test_get_dimensions_by_label(self):
        """ Test pyjstat get_dimensions() using label as parameter """

        dimensions, dim_names = pyjstat.get_dimensions(
            self.oecd_datasets['oecd'], 'label')
        self.assertTrue(dim_names[2] == '2003-2014')
        self.assertTrue(dimensions[0].iloc[0]['label'] == 'unemployment rate')

    def test_get_dimensions_by_index(self):
        """ Test pyjstat get_dimensions() using id as parameter """

        dimensions, dim_names = pyjstat.get_dimensions(
            self.oecd_datasets['oecd'], 'index')
        self.assertTrue(dim_names[2] == 'year')
        self.assertTrue(dimensions[0].iloc[0]['index'] == 0)

    def test_get_df_row(self):
        """ Test pyjstat get_df_row() """

        dimensions = pyjstat.get_dimensions(self.oecd_datasets['oecd'],
                                            'label')
        first_row = ['unemployment rate', 'Australia', '2003']
        categories = pyjstat.get_df_row(dimensions[0])
        self.assertTrue(set(first_row) == set(next(categories)))

    def test_get_values(self):
        """ Test pyjstat get_values() """

        values = pyjstat.get_values(self.oecd_datasets['oecd'])
        first_four_values = [5.943826289, 5.39663128, 5.044790587, 4.789362794]
        last_four_values = [7.953121271, 7.970392182, 8.15379125, 8.004598637]
        self.assertTrue(set(first_four_values) == set(values[:4]))
        self.assertTrue(set(last_four_values) == set(values[-4:]))

        ons_values = pyjstat.get_values(self.ons_datasets['ST1117EWla'])
        first_four_ons_values = [195074, 96699, 98375, 1524]
        last_four_ons_values = [30, 234, 101, 133]
        self.assertTrue(set(first_four_ons_values) == set(ons_values[:4]))
        self.assertTrue(set(last_four_ons_values) == set(ons_values[-4:]))

    def test_uniquify(self):
        """ Test pyjstat uniquify() """

        input_list = [1, 4, 5, 5, 3]
        output_list = [1, 4, 5, 3]
        self.assertTrue(set(input_list) == set(output_list))

    def test_from_json_stat_with_label(self):
        """ Test pyjstat from_json_stat() using label as parameter """

        results = pyjstat.from_json_stat(self.oecd_datasets)
        line_thirty = ['unemployment rate', 'Belgium', '2009', 7.891892855]
        dimensions = pyjstat.get_dimensions(self.oecd_datasets['oecd'],
                                            'label')
        self.assertTrue(len(results) == 2)
        self.assertTrue(set(results[0].columns.values[:-1]) ==
                        set(dimensions[1]))
        self.assertTrue(set(results[0].iloc[30].values) ==
                        set(line_thirty))

    def test_from_json_stat_with_id(self):
        """ Test pyjstat from_json_stat() using id as parameter"""

        results = pyjstat.from_json_stat(self.oecd_datasets, naming='id')
        line_thirty = [u'UNR', u'BE', u'2009', 7.891892855]
        dimensions = pyjstat.get_dimensions(self.oecd_datasets['oecd'], 'id')
        self.assertTrue(len(results) == 2)
        self.assertTrue(set(results[0].columns.values[:-1]) ==
                        set(dimensions[1]))
        self.assertTrue(set(results[0].iloc[30].values) ==
                        set(line_thirty))

    def test_to_json_stat(self):
        """ Test pyjstat to_json_stat()"""

        results = pyjstat.from_json_stat(self.oecd_datasets)
        json_data = json.loads(pyjstat.to_json_stat(results),
                               object_pairs_hook=OrderedDict)
        self.assertTrue(json_data[0]["dataset1"]["dimension"]
                        ["indicator"]["label"] ==
                        "indicator")
        self.assertTrue(json_data[0]["dataset1"]["dimension"]["size"][1] == 36)
        self.assertTrue(json_data[1]["dataset2"]["dimension"]["id"][2] ==
                        "age group")
        self.assertTrue(json_data[0]["dataset1"]["value"][-1],
                        results[0][-1:]['value'])
        results[0].columns = ['a', 'a', 'b', 'value']
        self.assertRaises(ValueError, pyjstat.to_json_stat, results)

    def test_to_json_stat_types(self):
        """ Test pyjstat to_json_stat() output types"""

        results = pyjstat.from_json_stat(self.oecd_datasets)
        json_data = json.loads(pyjstat.to_json_stat(results),
                               object_pairs_hook=OrderedDict)
        self.assertTrue(json_data[0]["dataset1"]["dimension"]
                        ["OECD countries, EU15 and total"]["category"]["index"]
                        ["Spain"] == 28)
        self.assertTrue(type(json_data[0]["dataset1"]["dimension"]
                             ["OECD countries, EU15 and total"]["category"]
                             ["index"]["Spain"]) is int)
        self.assertTrue(json_data[0]["dataset1"]["dimension"]
                        ["OECD countries, EU15 and total"]["category"]["label"]
                        ["France"] == "France")
        self.assertTrue(type(str(json_data[0]["dataset1"]["dimension"]
                                 ["OECD countries, EU15 and total"]["category"]
                                 ["label"]["France"])) is str)
        self.assertTrue(json_data[0]["dataset1"]["dimension"]["2003-2014"]
                        ["category"]["index"]["2005"] == 2)
        self.assertTrue(json_data[0]["dataset1"]["dimension"]["2003-2014"]
                        ["category"]["label"]["2005"] == "2005")
        self.assertTrue(type(json_data[0]["dataset1"]["dimension"]
                             ["2003-2014"]["category"]["index"]["2005"])
                        is int)
        self.assertTrue(type(str(json_data[0]["dataset1"]["dimension"]
                                 ["2003-2014"]["category"]["label"]["2005"]))
                        is str)

    def test_to_json_stat_value(self):
        """ Test pyjstat to_json_stat() custom value column"""

        results = pyjstat.from_json_stat(self.sample_dataset, value='measure')
        json_data = json.loads(pyjstat.to_json_stat(results, value='measure'),
                               object_pairs_hook=OrderedDict)
        self.assertTrue(json_data[0]["dataset1"]["measure"][0] == 4729)

    def test_from_to_json_stat_as_dict(self):
        """ Test pyjstat nested from-to json_stat using dict of dicts as input
        """

        results = pyjstat.from_json_stat(self.oecd_datasets)
        json_data = json.loads(pyjstat.to_json_stat(results, output='dict'),
                               object_pairs_hook=OrderedDict)
        data_df = pyjstat.from_json_stat(
            json.loads(json.dumps(json_data), object_pairs_hook=OrderedDict))
        line_thirty = ['unemployment rate', 'Belgium', '2009', 7.891892855]
        dimensions = pyjstat.get_dimensions(self.oecd_datasets['oecd'],
                                            'label')
        self.assertTrue(len(data_df) == 2)
        self.assertTrue(set(data_df[0].columns.values[:-1]) ==
                        set(dimensions[1]))
        self.assertTrue(set(data_df[0].iloc[30].values) ==
                        set(line_thirty))

    def test_from_to_json_stat_as_list(self):
        """ Test pyjstat nested from-to json_stat using list of dicts as input
        """

        results = pyjstat.from_json_stat(self.oecd_datasets)
        json_data = json.loads(pyjstat.to_json_stat(results),
                               object_pairs_hook=OrderedDict)
        data_df = pyjstat.from_json_stat(
            json.loads(json.dumps(json_data), object_pairs_hook=OrderedDict))
        line_thirty = ['unemployment rate', 'Belgium', '2009', 7.891892855]
        dimensions = pyjstat.get_dimensions(self.oecd_datasets['oecd'],
                                            'label')
        self.assertTrue(len(data_df) == 2)
        self.assertTrue(set(data_df[0].columns.values[:-1]) ==
                        set(dimensions[1]))
        self.assertTrue(set(data_df[0].iloc[30].values) ==
                        set(line_thirty))

    def test_from_to_json_stat_no_loads(self):
        """ Test pyjstat nested from-to json_stat using list of dicts as input
        """

        results = pyjstat.from_json_stat(self.oecd_datasets)
        json_data = json.loads(pyjstat.to_json_stat(results),
                               object_pairs_hook=OrderedDict)
        data_df = pyjstat.from_json_stat(json_data)
        line_thirty = ['unemployment rate', 'Belgium', '2009', 7.891892855]
        dimensions = pyjstat.get_dimensions(self.oecd_datasets['oecd'],
                                            'label')
        self.assertTrue(len(data_df) == 2)
        self.assertTrue(set(data_df[0].columns.values[:-1]) ==
                        set(dimensions[1]))
        self.assertTrue(set(data_df[0].iloc[30].values) ==
                        set(line_thirty))

    def test_generate_df_with_label(self):
        """ Test pyjstat generate_df() using label as parameter"""

        data_df = pyjstat.generate_df(self.oecd_datasets['oecd'], 'label')
        line_thirty = ['unemployment rate', 'Belgium', '2009', 7.891892855]
        dimensions = pyjstat.get_dimensions(self.oecd_datasets['oecd'],
                                            'label')
        self.assertTrue(set(data_df.columns.values[:-1]) ==
                        set(dimensions[1]))
        self.assertTrue(set(data_df.iloc[30].values) ==
                        set(line_thirty))

    def test_generate_df_with_id(self):
        """ Test pyjstat generate_df() using id as parameter"""

        data_df = pyjstat.generate_df(self.oecd_datasets['oecd'], 'id')
        line_thirty = ['UNR', 'BE', '2009', 7.891892855]
        dimensions = pyjstat.get_dimensions(self.oecd_datasets['oecd'], 'id')
        self.assertTrue(set(data_df.columns.values[:-1]) ==
                        set(dimensions[1]))
        self.assertTrue(set(data_df.iloc[30].values) ==
                        set(line_thirty))

    def test_class_dataset(self):
        """ Test pyjstat using class dataset from v1.02"""

        results = pyjstat.from_json_stat(self.galicia_dataset)
        json_data = json.loads(pyjstat.to_json_stat(results, output='dict'),
                               object_pairs_hook=OrderedDict)
        self.assertTrue(self.galicia_dataset['class'] == 'dataset')
        self.assertTrue(len(results[0].columns) == 7)
        self.assertTrue(len(results[0].index) == 3960)
        self.assertTrue(self.galicia_dataset['value'][0] ==
                        json_data['dataset1']['value'][0])
        self.assertTrue(self.galicia_dataset['value'][547] ==
                        json_data['dataset1']['value'][547])
        self.assertTrue(self.galicia_dataset['value'][-1] ==
                        json_data['dataset1']['value'][-1])

    def test_uk_dataset(self):
        """ Test pyjstat using a different ONS dataset"""

        results = pyjstat.from_json_stat(self.uk_dataset)
        json_data = json.loads(pyjstat.to_json_stat(results, output='dict'),
                               object_pairs_hook=OrderedDict)
        self.assertTrue(len(results[0].columns) == 5)
        self.assertTrue(len(results[0].index) == 3)
        self.assertTrue(self.uk_dataset['QS104EW']['value']['0'] ==
                        json_data['dataset1']['value'][0])
        self.assertTrue(self.uk_dataset['QS104EW']['value']['2'] ==
                        json_data['dataset1']['value'][2])

    def test_us_labor_dataset(self):
        """ Test pyjstat using a us labor dataset of class dataset"""

        results = pyjstat.from_json_stat(self.uslabor_dataset)
        json_data = json.loads(pyjstat.to_json_stat(results, output='dict'),
                               object_pairs_hook=OrderedDict)
        self.assertTrue(self.uslabor_dataset['class'] == 'dataset')
        self.assertTrue(len(results[0].columns) == 4)
        self.assertTrue(len(results[0].index) == 12880)
        self.assertTrue(self.uslabor_dataset['value'][0] ==
                        json_data['dataset1']['value'][0])
        self.assertTrue(self.uslabor_dataset['value'][547] ==
                        json_data['dataset1']['value'][547])
        self.assertTrue(self.uslabor_dataset['value'][-1] ==
                        json_data['dataset1']['value'][-1])

    def test_convert_zeroes_not_null(self):
        """ Test pyjstat to_json_stat zero conversion"""

        results = pyjstat.from_json_stat(self.sweden_dataset)
        json_data = json.loads(pyjstat.to_json_stat(results, output='dict'),
                               object_pairs_hook=OrderedDict)
        self.assertTrue(self.sweden_dataset['dataset']['value'][0] ==
                        json_data['dataset1']['value'][0])

    def test_from_json_stat_no_coertion(self):
        """ Test pyjstat from_json_stat with id naming without coertion"""

        results = pyjstat.from_json_stat(self.sweden_dataset, naming='id')
        self.assertTrue(results[0]['Alder'][500] == '35-39')

    def test_ons_index_sort_bug(self):
        """ Test pyjstat from_json_stat dimension sorting"""
        results = pyjstat.from_json_stat(self.ons_dataset)
        json_data = json.loads(pyjstat.to_json_stat(results, output='dict'),
                               object_pairs_hook=OrderedDict)
        self.assertTrue(self.ons_dataset['A02Level']['dimension']['CL_0000667']
                        ['category']['index']['CI_0018938'] ==
                        json_data['dataset1']['dimension']['Age']['category']
                        ['index']['16-17'])

    def test_ons_index_sort_bug_index(self):
        """ Test pyjstat from_json_stat dimension sorting using indexes
        instead of labels"""
        results = pyjstat.from_json_stat(self.ons_dataset, naming='id')
        json_data = json.loads(pyjstat.to_json_stat(results, output='dict'),
                               object_pairs_hook=OrderedDict)
        self.assertTrue(self.ons_dataset['A02Level']['dimension']['CL_0000667']
                        ['category']['index']['CI_0018938'] ==
                        json_data['dataset1']['dimension']['CL_0000667']
                        ['category']['index']['CI_0018938'])

if __name__ == '__main__':
    unittest.main()
