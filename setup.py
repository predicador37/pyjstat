# -*- coding: utf-8 -*-
"""pyjstat package setup."""
from setuptools import setup

setup(
    name='pyjstat',
    version='2.3.0',
    author='Miguel Expósito Martín',
    author_email='miguel.exposito@gmail.com',
    packages=['pyjstat', 'pyjstat.test'],
    url='https://github.com/predicador37/pyjstat',
    license='Apache License 2.0',
    description='Library to handle JSON-stat data in python using pandas '
                'DataFrames.',
    long_description=open('README.rst').read(),
    install_requires=[
        'pandas', 'requests'
    ],
    test_suite='pyjstat.test',
    keywords=['json-stat', 'json', 'statistics', 'dataframe', 'converter'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries'
    ],
)
