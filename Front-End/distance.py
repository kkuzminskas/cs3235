
import prep_data
import dist_analysis
import json
import numpy as np


def extract_norm_x_y_t(filename):

    try:
        file = open(filename, "r")
        data = file.read()
        data = json.loads(data)['all']
    except:
        prep_data.clean_data(filename)
        return extract_norm_x_y_t

    tracking_data = [l for l in data if l['category'] ==
                     "tracker" and l['values']['frame']['state'] == 7]

    time_stamps = np.array([l['values']['frame']['time']
                            for l in tracking_data])
    time_stamps = time_stamps - time_stamps[0]

    x_y_data = np.array([(l['values']['frame']['avg']['x'],
                          l['values']['frame']['avg']['y']) for l in tracking_data])
    x_y_t = np.concatenate((x_y_data, time_stamps.T.reshape((len(x_y_data), 1))), axis=1)

    return dist_analysis.whiten(x_y_t)


def eyenalysis(filename):
    reference_files = [f"../data/siqi{i+1}.txt" for i in range(8)]
    norm_x_y_t = extract_norm_x_y_t(filename)
    sum = 0
    for f in reference_files:
        ref_norm_x_y_t = extract_norm_x_y_t(f)
        sum += dist_analysis.eyenalysis_distance(norm_x_y_t, ref_norm_x_y_t)

    # threshold determined experimentally
    #return (sum / len(reference_files)) < 0.78549708
    return (sum /len(reference_files)) <0.70588