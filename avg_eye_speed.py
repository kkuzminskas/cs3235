import numpy as np
import json 
import pandas as pd
import math


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

def avg_eye_speed(data, np_data, np_time):
    np_x = np.array(data['avg_x'])
    np_y = np.array(data['avg_y'])
    np_time = np.array(data['time'])

    prev_x = np_x[0]
    prev_y = np_y[0]

    prev_time = np_time[0]
    np_time = np_time - prev_time
    prev_time = np_time[0]

    speed_lst = []

    for ind, val in enumerate(np_x[1::]):
        curr_x = val
        curr_y = np_y[ind + 1]
        curr_time = np_time[ind + 1]

        distance = math.sqrt((curr_x - prev_x)**2 + (curr_y - prev_y)**2)
        time_dif = curr_time - prev_time

        speed = distance/time_dif
        speed_lst.append(speed)

    return np.array(speed_lst).mean()



if __name__ == '__main__':
    data = clean_data()
    np_data = np.array(data)
    np_time = np.array(data['time'])


    avg_speed = avg_eye_speed(data, np_data, np_time)
    print(avg_speed)
