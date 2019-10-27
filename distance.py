
import json 
import os
import numpy as np 

os.chdir("/home/ahmed/cs3235/proj/cs3235")

def extract_x_y (filename):
    file = open(filename, "r")
    data = file.read()
    data = json.loads(data)['all']
    eye_x_y_list = [l for l in data if l['category']=="tracker"]
    return [(l['values']['frame']['avg']['x'],l['values']['frame']['avg']['y']) for l in eye_x_y_list]
    
def find_best (reference,compared):
    def calculate_min (a):
        return  np.sqrt(((compared - a)**2).sum(axis=1)).min()

    return np.array ([calculate_min(a) for a in reference])

def eyenalysis_distance (file_1, file_2):
    values1 = np.array (extract_x_y (file_1))
    values2 = np.array (extract_x_y (file_2))
    best_1 = find_best(values1, values2)
    best_2 = find_best(values2, values1)
    norm_factor = len(values1) if len(values1) > len(values2) else len(values2)
    return (best_1.sum() + best_2.sum()) / norm_factor
    
    
print(eyenalysis_distance("eyetribe_output.txt","eyetribe_output.txt")) # should be zero 


