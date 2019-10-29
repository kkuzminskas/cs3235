import pandas as pd
import numpy as np
import json
import os


def transform_file(file_name="eyetribe_output_copy.txt"):
    file = open(file_name, "r+")
    content = ""
    for line in file:
        content += line[:-1] + ", \n"
    content = content[:-3] + "\n]}"
    file.seek(0,0)
    file.write('{"all": [\n' + content)
    file.close()

# Get data
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


def clean_data(file_name="eyetribe_output_test.txt"):
    transform_file(file_name)

    files = open(file_name, "r")
    data = files.read()
    d2 = json.loads(data)
    files.close()

    output_list = d2['all']
    final_output = {}

    ## Preprocessing Data
    keys = list(output_list[0]['values']['frame'].keys())

    empty_list('', keys, final_output, output_list[0]['values']['frame'])

    
    for val in output_list:
        if 'values' in val.keys():
            transform_vals('', keys, final_output, val['values']['frame'])

    pd_data = pd.DataFrame.from_dict(final_output)
    features = ["time", "avg_x", "avg_y"]
    return pd_data[features]




if __name__ == '__main__':
    # get data
    # data = clean_data("eyetribe_output_copy.txt")
    data = clean_data("eyetribe_output_copy.txt")
    
