# import pygaze
import pandas as pd
import numpy as np
import json
from my_constants import *
# from pywin32 import GetSystemMetrics
import time
import prep_data as prep


# TODO: have calibration at beginning of pin detection, set frame rate to 60
# TODO: integrate w/ flask interactively

# get the pin value
def num_val(x, y, w_split, h_split):
    pin = 0
    if (x < w_split):
        if (y < h_split): # + TOP):
            pin = 1
        elif (y < 2*h_split): # + TOP):
            pin = 4
        else:
            pin = 7
    elif (x < 2*w_split):
        if (y < h_split): # + TOP):
            pin = 2
        elif (y < 2*h_split):# + TOP):
            pin = 5
        else:
            pin = 8
    else:
        if (y < h_split):# + TOP):
            pin = 3
        elif (y < 2*h_split): # + TOP):
            pin = 6
        else:
            pin = 9
    
    return pin


def verify_pin(val, prev_time, prev_pins, old_data):
    # get the dimensions of the grid
    w_split = WIDTH/3
    h_split = (HEIGHT - TOP)/3

    time = val[0]
    x = val[1]
    y = val[2]
    
    # get the pin value
    curr_pin = num_val(x, y, w_split, h_split)

    

    time_dif = time - prev_time

    if time_dif > MIN_TIME:
        np_pins = np.array(prev_pins)
        unique_pins, pin_count = np.unique(np_pins, return_counts=True)
        # print(unique_pins, pin_count)
        max_ind = np.argmax(pin_count)
        # print(unique_pins[max_ind])
        # for old data, pin is found with curr_pin
        ret_pin = unique_pins[max_ind]
        if old_data:
            ret_pin = curr_pin
        return [True, ret_pin, time]
    
    return [False, curr_pin]

def simulate_real_data(data, np_data, old_data=False):

    prev_time = np.array(data['time'])[0]
    prev_pin = 0
    
    pin = ''
    prev_pins = []

    for ind, val in enumerate(np_data):
        verified = verify_pin(val, prev_time, prev_pins, old_data)
        prev_pin = verified[1]

        prev_pins.append(prev_pin)

        if verified[0]:
            prev_time = verified[2]
            pin += str(verified[1])
            prev_pins = []

    return pin

def test_pin_route(file='../k1.txt'):
    data = prep.clean_data(file)
    np_data = np.array(data)
    np_time = np.array(data['time'])
   
    pin = simulate_real_data(data, np_data)
    return pin, data
    # real_pin = get_pin(data, np_data, np_time)
