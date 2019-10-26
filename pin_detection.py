import pygaze
import pandas as pd
import numpy as np
import json
from win32api import GetSystemMetrics


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


def duplicate_pin(pin, pins, time_dif, time_inc):
    if time_dif > time_inc*1.5:
        pins.append(pin)
        duplicate_pin(pin, pins, time_dif - time_inc, time_inc)
    
    else:
        pins.append(pin)
    return pins

# get the pin value
def num_val(x, y, w_split, h_split):
    pin = 0
    if (x < w_split):
        if (y < h_split):
            pin = 7
        elif (y < 2*h_split):
            pin = 4
        else:
            pin = 1
    elif (x < 2*w_split):
        if (y < h_split):
            pin = 8
        elif (y < 2*h_split):
            pin = 5
        else:
            pin = 2
    else:
        if (y < h_split):
            pin = 9
        elif (y < 2*h_split):
            pin = 6
        else:
            pin = 3
    
    return pin


def get_pin(data, np_data, np_time):
    # get the size of the screen
    width = GetSystemMetrics(0)
    height =  GetSystemMetrics(1)

    # get the dimensions of the grid
    w_split = width/3
    h_split = height/3


    # Get the total time and approximate increment for time
    start_time = np_time[0]
    end_time = np_time[len(np_time)-1]
    total_time = end_time - start_time
    pin_length = 6


    time_inc = total_time/pin_length

    prev_pin = 0

    switch_ind = []
    dif_pin = []
    dif_time = []

    time_dif = 0
    prev_start = 0

    for ind, val in enumerate(np.array(data)):
        time = val[0] - start_time
        x = val[1]
        y = val[2]

        curr_pin = num_val(x, y, w_split, h_split)
        # temp_pin.append(curr_pin)

        if curr_pin != prev_pin:
            switch_ind.append(ind)
            dif_pin.append(curr_pin)

            time_dif = time - prev_start
            prev_start = time
            dif_time.append(time_dif) 

        prev_pin = curr_pin

    dif_time.append(time - prev_start)
    dif_time = dif_time[1::]


    real_pin = []


    for ind, pin in enumerate(dif_pin):
        time_dif = dif_time[ind]
        duplicate_pin(pin, real_pin, time_dif, time_inc)

    if len(real_pin) < pin_length:
        print("Error: wrong length pin. Try again")

    return real_pin



if __name__ == '__main__':
    # get data
    data = clean_data()
    np_data = np.array(data)
    np_time = np.array(data['time'])
    real_pin = get_pin(data, np_data, np_time)

    print(real_pin)





