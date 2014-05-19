# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='pyjstat',
    version='0.1.0',
    author='Miguel Expósito Martín',
    author_email='miguel.exposito@gmail.com',
    packages=['pyjstat', 'pyjstat.test'],
    #scripts=['bin/example.py'],
    url='http://pypi.python.org/pypi/pyjstat/',
    license='LICENSE',
    description='Module to handle JSON-stat in python pandas.',
    long_description=open('README.rst').read(),
    install_requires=[
       'pandas'
    ],
    test_suite='pyjstat.test',
    keywords=['json-stat', 'json', 'statistics', 'dataframe', 'converter']
)
