simport prep_data
import json
import numpy as np
import os
import sys


def whiten(values):
    column_std_dev = np.std(values, axis=0)
    # for constant columns with zero variance
    column_std_dev[column_std_dev == 0] = 1
    return values / (column_std_dev)


def extract_fix_d_bool(values, fixations):
    x_sum = y_sum = num_points = start_t = last_t = 0
    prev_fix = False
    res = []
    for i, val in enumerate(values):
        cur_fix = fixations[i]
        if cur_fix:
            if prev_fix:
                x_sum += val[0]
                y_sum += val[1]
                last_t = val[2]
                num_points += 1
            else:
                x_sum = val[0]
                y_sum = val[1]
                last_t = start_t = val[2]
                num_points = 1
        else:
            if prev_fix:
                res.append((x_sum/num_points, y_sum /
                            num_points, last_t-start_t))
        prev_fix = cur_fix

    # case where input ends with a fixation
    if prev_fix:
        res.append((x_sum/num_points, y_sum /
                    num_points, last_t-start_t))

    return np.array(res)


# def extract_point_avg_speed(values):


def extract_features(filename, coord_type):
    try:
        file = open(filename, "r")
        data = file.read()
        data = json.loads(data)['all']
    except:
        prep_data.clean_data(filename)
        return extract_features(filename, coord_type)

    tracking_data = [l for l in data if l['category'] ==
                     "tracker" and l['values']['frame']['state'] == 7]

    # time stamps
    time_stamps = np.array([l['values']['frame']['time']
                            for l in tracking_data])
    # start counting time relative to the first point
    time_stamps = time_stamps - time_stamps[0]

    # (x,y)
    x_y_data = np.array([(l['values']['frame'][coord_type]['x'],
                          l['values']['frame'][coord_type]['y']) for l in tracking_data])

    #left (x,y)
    l_x_y_data = np.array([(l['values']['frame']['lefteye'][coord_type]['x'],
                            l['values']['frame']['lefteye'][coord_type]['y']) for l in tracking_data])
    #right (x,y)
    r_x_y_data = np.array([(l['values']['frame']['righteye'][coord_type]['x'],
                            l['values']['frame']['righteye'][coord_type]['y']) for l in tracking_data])
    f_data = np.array([l['values']['frame']['fix']
                       for l in tracking_data])
    return x_y_data, time_stamps, l_x_y_data, r_x_y_data, f_data


def find_best(reference, compared):
    def calculate_min(a):
        return np.sqrt(((compared - a)**2).sum(axis=1)).min()
    return np.array([calculate_min(a) for a in reference])


def eyenalysis_distance(values1, values2):
    best_1 = find_best(values1, values2)
    best_2 = find_best(values2, values1)
    norm_factor = len(values1) if len(values1) > len(values2) else len(values2)
    return (best_1.sum() + best_2.sum()) / norm_factor


def try_distances(file1, file2, coord_type):

    # extract relevant columns
    x_y_1, t_1, l_x_y_1, r_x_y_1, f_1 = extract_features(file1, coord_type)
    x_y_2, t_2, l_x_y_2, r_x_y_2, f_2 = extract_features(file2, coord_type)

    print(f"{coord_type} Measurements:")

    # simple Eyenalysis distance with only (x,y) coordinates
    print("     x,y distance :" + str(eyenalysis_distance(x_y_1, x_y_2)))

    # add the timestamp column
    x_y_t_1 = np.concatenate((x_y_1, t_1.T.reshape((len(x_y_1), 1))), axis=1)
    x_y_t_2 = np.concatenate((x_y_2, t_2.T.reshape((len(x_y_2), 1))), axis=1)

    print("     x,y,t (non whitened) distance :" +
          str(eyenalysis_distance(x_y_t_1, x_y_t_2)))

    # "whiten" the data, remove the unit problem (milliseconds and pixels) by dividing each column by its standard deviation
    norm_x_y_t_1 = whiten(x_y_t_1)
    norm_x_y_t_2 = whiten(x_y_t_2)
    print("     x,y,t distance (whitened):" +
          str(eyenalysis_distance(norm_x_y_t_1, norm_x_y_t_2)))

    # extract fixations using boolean provided by the EyeTribe
    f_d_1 = extract_fix_d_bool(x_y_t_1, f_1)
    f_d_2 = extract_fix_d_bool(x_y_t_2, f_2)
    norm_f_d_1 = whiten(f_d_1)
    norm_f_d_2 = whiten(f_d_2)
    print("     x,y,d distance (using boolean) :" +
          str(eyenalysis_distance(norm_f_d_1, norm_f_d_2)))

    # add left and right eye positions
    x_y_lx_ly_1 = np.concatenate((x_y_1, l_x_y_1), axis=1)
    x_y_lx_ly_rx_ry_1 = np.concatenate((x_y_1, r_x_y_1), axis=1)

    x_y_lx_ly_2 = np.concatenate((x_y_2, l_x_y_2), axis=1)
    x_y_lx_ly_rx_ry_2 = np.concatenate((x_y_2, r_x_y_2), axis=1)
    print("     x,y,lx,ly,ry,ry :" +
          str(eyenalysis_distance(x_y_lx_ly_rx_ry_1, x_y_lx_ly_rx_ry_2)))

    # group fixations into one row and convert the timestamp into fixation duration
    # f_d_1 = extract_fix_d(x_y_t_1)
    # f_d_2 = extract_fix_d(x_y_t_2)
    # norm_f_d_1 = whiten(f_d_1)
    # norm_f_d_2 = whiten(f_d_2)
    # print("     x,y,d distance :" +
    #       str(eyenalysis_distance(norm_f_d_1, norm_f_d_2)))

    return
    # TEST print(eyenalysis_distance(x_y_1,x_y_1) == 0)
    # TEST print(np.std(norm_y_y_t_1,axis=0)); should be [1,1,1]
    # TEST print(eyenalysis_distance(norm_x_y_t_1,norm_x_y_t_1) == 0)
    # TEST print(eyenalysis_distance(norm_f_d_1, norm_f_d_1) == 0)


def main(file1, file2):
    try_distances(file1, file2, 'avg')
    try_distances(file1, file2, 'raw')


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
