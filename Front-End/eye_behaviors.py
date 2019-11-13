import joblib
import pandas as pd
import numpy as np
import math
from prep_data import clean_data


def sign(x):
    if (x > 0):
        return 1
    elif (x == 0):
        return 0
    return -1

def calc_distance(curr_x, prev_x, curr_y, prev_y):
    distance = math.sqrt((curr_x - prev_x)**2 + (curr_y - prev_y)**2)
    return distance

def velocity(distance, change_time):
    return distance/change_time

def acceleration(prev_v, curr_v, change_time):
    return (curr_v-prev_v)/change_time

def avg_eye_speed(data):
    np_x = np.array(data['avg_x'])
    np_y = np.array(data['avg_y'])
    np_time = np.array(data['time'])
    # np_left_x = np.array(data['lefteye_avg_x'])
    # np_left_y= np.array(data['lefteye_avg_y'])
    # np_right_x= np.array(data['righteye_avg_x'])
    # np_right_y= np.array(data['righteye_avg_y'])

    prev_x = np_x[0]
    prev_y = np_y[0]

    prev_time = np_time[0]
    np_time = np_time - prev_time
    prev_time = np_time[0]

    speed_lst = []
    distance_lst = []
    eye_direct_lst = []
    eye_distance_lst = []

    for ind, val in enumerate(np_x[1::]):
        curr_x = val
        curr_y = np_y[ind + 1]
        curr_time = np_time[ind + 1]

        distance = calc_distance(curr_x, prev_x, curr_y, prev_y)
        time_dif = curr_time - prev_time

        speed = velocity(distance, time_dif)

        # change_x = curr_x-prev_x
        # change_y = curr_y - prev_y
        # v_x = velocity(change_x, time_dif)
        # v_y = velocity(change_y, time_dif)
        # eye_direct = eye_direction(change_x, change_y, v_x, v_y)

        # eye_distance = avg_eye_distance(np_right_x[ind], np_left_x[ind], np_right_y[ind], np_left_y[ind])

        # eye_direct_lst.append(eye_direct)
        speed_lst.append(speed)
        distance_lst.append(distance)
        # eye_distance_lst.append(eye_distance)

    means = [np.array(speed_lst).mean(), np.array(distance_lst).mean()]#, np.array(eye_distance_lst).mean()]
    # signal = sum(speed_lst)/sum(eye_direct_lst)
    return means[0], means[1]#, signal*(10**5)#, np.array(eye_direct_lst).mean()#, means[2]


def check_eye_behavior(user, data):
    loaded_model = joblib.load('eye_behaviors_model.sav')
    speed, distance = avg_eye_speed(data)
    x_test =pd.DataFrame({
        'avg_speed': list([speed]),
        'avg_dist': list([distance])
    })
    pred = loaded_model.predict(x_test)
    print("EYE BEHAVIOR")
    print(user)
    print(pred)
    return pred == user
    
