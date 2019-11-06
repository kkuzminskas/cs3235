
import matplotlib
import numpy as np

# save thresholds
import pickle
import prep_data
import json
import numpy as np



#devides each column of data by its standard deviations
def whiten(values):
    column_std_dev = np.std(values, axis=0)
    # for constant columns with zero variance
    column_std_dev[column_std_dev == 0] = 1
    return values / (column_std_dev)

#extracts fixations and their duration out of data in (x,y,t) format
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

    # left (x,y)
    l_x_y_data = np.array([(l['values']['frame']['lefteye'][coord_type]['x'],
                            l['values']['frame']['lefteye'][coord_type]['y']) for l in tracking_data])
    # right (x,y)
    r_x_y_data = np.array([(l['values']['frame']['righteye'][coord_type]['x'],
                            l['values']['frame']['righteye'][coord_type]['y']) for l in tracking_data])
    f_data = np.array([l['values']['frame']['fix']
                       for l in tracking_data])
    return x_y_data, time_stamps, l_x_y_data, r_x_y_data, f_data


def find_best(reference, compared):
    def calculate_min(a):
        return np.sqrt(((compared - a)**2).sum(axis=1)).min()
    return np.array([calculate_min(a) for a in reference])

#calculate the eyenalysis distance between two sets of eye mouvements
def eyenalysis_distance(values1, values2):
    best_1 = find_best(values1, values2)
    best_2 = find_best(values2, values1)
    norm_factor = len(values1) if len(values1) > len(values2) else len(values2)
    return (best_1.sum() + best_2.sum()) / norm_factor

#calculates different distance metrics for two files
def try_distances(file1, file2, coord_type):

    # extract relevant columns
    x_y_1, t_1, l_x_y_1, r_x_y_1, f_1 = extract_features(file1, coord_type)
    x_y_2, t_2, l_x_y_2, r_x_y_2, f_2 = extract_features(file2, coord_type)

    # simple Eyenalysis distance with only (x,y) coordinates
    x_y_distance = eyenalysis_distance(x_y_1, x_y_2)

    # add the timestamp column
    x_y_t_1 = np.concatenate((x_y_1, t_1.T.reshape((len(x_y_1), 1))), axis=1)
    x_y_t_2 = np.concatenate((x_y_2, t_2.T.reshape((len(x_y_2), 1))), axis=1)

    x_y_t_no_whiten_distance = eyenalysis_distance(x_y_t_1, x_y_t_2)

    # "whiten" the data, remove the unit problem (milliseconds and pixels) by dividing each column by its standard deviation
    norm_x_y_t_1 = whiten(x_y_t_1)
    norm_x_y_t_2 = whiten(x_y_t_2)
    x_y_t_withen_distance = eyenalysis_distance(norm_x_y_t_1, norm_x_y_t_2)

    # extract fixations using boolean provided by the EyeTribe
    f_d_1 = extract_fix_d_bool(x_y_t_1, f_1)
    f_d_2 = extract_fix_d_bool(x_y_t_2, f_2)
    f_d_no_whiten_distance = eyenalysis_distance(f_d_1, f_d_2)

    norm_f_d_1 = whiten(f_d_1)
    norm_f_d_2 = whiten(f_d_2)
    f_d_whiten_distance = eyenalysis_distance(norm_f_d_1, norm_f_d_2)
    
    # add left and right eye positions
    x_y_lx_ly_1 = np.concatenate((x_y_1, l_x_y_1), axis=1)
    x_y_lx_ly_rx_ry_1 = np.concatenate((x_y_lx_ly_1, r_x_y_1), axis=1)

    x_y_lx_ly_2 = np.concatenate((x_y_2, l_x_y_2), axis=1)
    x_y_lx_ly_rx_ry_2 = np.concatenate((x_y_lx_ly_2, r_x_y_2), axis=1)

    x_y_lx_ly_rx_ry_distance = eyenalysis_distance(
        x_y_lx_ly_rx_ry_1, x_y_lx_ly_rx_ry_2)

    return np.array([x_y_distance, x_y_t_no_whiten_distance, x_y_t_withen_distance,
                     x_y_lx_ly_rx_ry_distance])

#calculates the average distance metrics from a new file to a set of reference files
def distances(reference_files, file, coord_type):
    num_files = len(reference_files)
    res = np.zeros(4)
    for i in range(num_files):
        dist = try_distances(reference_files[i], file, coord_type)
        res = res + dist
    return res / num_files




def determine_thresholds(reference_files):
    
    training_neg_files = ["youkuan1.txt", "youkuan2.txt", "youkuan3.txt", "youkuan4.txt", "youkuan5.txt",
                          "siqi1.txt", "siqi2.txt", "siqi3.txt", "siqi4.txt", "siqi5.txt", "ahmed1.txt"]
    training_pos_files = ["data/k9.txt", "data/k10.txt", "data/k11.txt"]
    training_neg_files = ["data/" + l for l in training_neg_files]

    neg_dist = np.array([distances(reference_files, l, 'raw')
                         for l in training_neg_files])
    pos_dist = np.array([distances(reference_files, l, 'raw') 
                         for l in training_pos_files])
    raw_thresholds = (neg_dist.min(axis=0) + pos_dist.max(axis=0)) / 2

    neg_dist = np.array([distances(reference_files, l, 'avg')
                         for l in training_neg_files])
    pos_dist = np.array([distances(reference_files, l, 'avg')
                         for l in training_pos_files])
    
    avg_thresholds = (neg_dist.min(axis=0) + pos_dist.max(axis=0)) / 2
    
    return avg_thresholds,raw_thresholds

#Takes in test_files and labels, classifies the files based on threshold and print information about the classification
#for each distance metric
def test_with_files(test_files, test_labels, raw_thresholds, avg_thresholds):

    def find_metrics(labels):
        positives = np.sum(labels)
        true_positives = np.sum(np.logical_and(test_labels == 1, labels == 1))
        false_positives = positives - true_positives

        negatives = len(test_labels) - positives
        true_negatives = np.sum(np.logical_and(test_labels == 0, labels == 0))
        false_negatives = negatives - true_negatives

        precision = true_positives / positives if positives != 0 else 1
        accuracy = (true_negatives + true_positives) / (positives + negatives)

        return true_positives, false_positives, true_negatives, false_negatives, accuracy, precision

    def print_results(coord_types, class_labels):
        dist_names = ["x_y distance", "x_y_t non whitened distance",
                      "x_y_t whitened distance", "x_y_lx_ly_rx_ry distance"]

        print("#####Results#####:")
        print(f"     {coord_types}:")
        for ind, labels in enumerate(class_labels):
            true_positives, false_positives, true_negatives, false_negatives, accuracy, precision = find_metrics(
                labels)
            print("     " + dist_names[ind])
            print(f"        true_positives  :{true_positives}")
            print(f"        false_positives :{false_positives}")
            print(f"        true_negatives  :{true_negatives}")
            print(f"        false_negatives :{false_negatives}")
            print(f"        Accuracy        :{accuracy}")
            print(f"        Precision       :{precision}")


    avg_distances = np.array([distances(reference_files, f, 'avg') for f in test_files]).T
    labels = np.zeros(avg_distances.shape)
    for i in range(4):
        labels[i][avg_distances[i] < avg_thresholds[i]] = 1
    print_results('avg', labels)

    raw_distances = np.array([distances(reference_files, f, 'raw') for f in test_files]).T
    labels = np.zeros(raw_distances.shape)
    for i in range(4):
        labels[i][raw_distances[i] < raw_thresholds[i]] = 1
    print_results('raw', labels)


def main ():
    reference_files = [f"data/k{i+1}.txt" for i in range(8)]
    avg_thresholds, raw_thresholds = determine_thresholds(reference_files)
    test_files = [f"data/k{12+i}.txt" for i in range(9)] + [f"data/siqi{10 + i}.txt" for i in range(6)] + [f"data/wanching{2 + i}.txt" for i in range(4)]
    labels = np.array([1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0])
    test_with_files(test_files, labels,raw_thresholds, avg_thresholds)
