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

# COLLECTION_URL = 'http://json-stat.org/samples/collection.json'
# collection = pyjstat.Collection.read(COLLECTION_URL)
#
# collection.write('dataframe_list')

EXAMPLE_URL = 'http://json-stat.org/samples/hierarchy.json'

dataset = pyjstat.Dataset.read(EXAMPLE_URL)
df = dataset.write('dataframe')
print(df)