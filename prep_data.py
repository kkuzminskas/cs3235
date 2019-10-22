import sklearn
import json
import pandas as pd
import numpy as np

files = open("eyetribe_output.txt", "r")
data = files.read()
d2 = json.loads(data)
files.close()

output_list = d2['all']
final_output = {}

## Preprocessing Data
keys = list(output_list[0]['values']['frame'].keys())


def empty_list(prev_key, keys, final_output, val):
    prev_key_init = prev_key
    for k in keys:
        prev_key = prev_key_init
        vals = val[k]
        if type(vals) == type({}):
            new_keys = vals.keys()
            prev_key += k + '_'
            empty_list(prev_key, new_keys, final_output, vals)
        else: 
            final_output[prev_key + k] = list()

empty_list('', keys, final_output, output_list[0]['values']['frame'])

def transform_vals(prev_key, keys, final_output, val):
    prev_key_init = prev_key
    for k in keys:
        prev_key = prev_key_init
        vals = val[k]
        if type(vals) == type({}):
            new_keys = vals.keys()
            prev_key += k + '_'
            transform_vals(prev_key, new_keys, final_output, vals)
        else: 
            final_output[prev_key + k].append(vals)

for val in output_list:
    if 'values' in val.keys():
        transform_vals('', keys, final_output, val['values']['frame'])

pd_data = pd.DataFrame.from_dict(final_output)
print(pd_data.head())

print(pd_data.columns.values.tolist())
print(pd_data.shape)

np_data = pd_data.to_numpy()

features = np.array(pd_data.columns.values.tolist())
remove_feat = ["fix", "time", "timestamp", "state"]
features = list(filter(lambda f: f not in remove_feat, features))
print(features)
# cleaned data with only float valued features
X = pd_data[features]
