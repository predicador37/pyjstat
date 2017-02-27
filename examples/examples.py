from pyjstat import pyjstat

# EXAMPLE_URL = 'http://json-stat.org/samples/galicia.json'
#
# dataset = pyjstat.Dataset.read(EXAMPLE_URL)
# df = dataset.write('dataframe')
# print(df)
#
# dataset_from_df = pyjstat.Dataset.read(df)
# print(dataset_from_df.write())
#
# EXAMPLE_URL = 'http://json-stat.org/samples/oecd.json'
# query = [{'concept': 'UNR'}, {'area': 'US'}, {'year': '2010'}]
#
# dataset = pyjstat.Dataset.read(EXAMPLE_URL)
# print(dataset.get_value(query))

from pyjstat import pyjstat

EXAMPLE_URL = 'http://json-stat.org/samples/collection.json'

collection = pyjstat.Collection.read(EXAMPLE_URL)
df_list = collection.write('dataframe_list')
print(df_list)

#
# EXAMPLE_URL = 'http://json-stat.org/samples/hierarchy.json'
#
# dataset = pyjstat.Dataset.read(EXAMPLE_URL)
# df = dataset.write('dataframe')
# print(df)


EXAMPLE_URL = 'http://web.ons.gov.uk/ons/api/data/dataset/DC1104EW.json?'\
              'context=Census&jsontype=json-stat&apikey=DCOpn8BU2i&'\
              'geog=2011HTWARDH&diff=&totals=false&'\
              'dm/2011HTWARDH=E12000007'
dataset = pyjstat.Dataset.read(EXAMPLE_URL)
df = dataset.write('dataframe')
print(df)