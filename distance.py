import json 
import os
import numpy as np 

os.chdir("/home/ahmed/cs3235/proj/cs3235")

def whiten (values):
    column_std_dev = np.std(values,axis=0)
    return values / column_std_dev

def extract_fix_d (values):
    def rec_extract (cur_x,cur_y,origin_t,last_t,values,res):
            if values.size == 0:
                res.append ((cur_x,cur_y,last_t-origin_t))
                return res
            else:
                (x,y,t) = values[0]
                if x==cur_x and y==cur_y:
                    return rec_extract (cur_x,cur_y,origin_t,t,values[1:],res)
                else:
                    res.append ((cur_x,cur_y,t-origin_t))
                    return rec_extract(x,y,t,t,values,res)
    
    if values.size == 0:
        return values
    else:
        res = []
        return np.array (rec_extract(0,0,0,0,values,res)[1:])

def extract_x_y (filename):
    file = open(filename, "r")
    data = file.read()
    data = json.loads(data)['all']
    eye_x_y_list = [l for l in data if l['category']=="tracker"]
    return np.array ([(l['values']['frame']['avg']['x'],l['values']['frame']['avg']['y']) for l in eye_x_y_list])

def extract_time (filename):
    file = open(filename, "r")
    data = file.read()
    data = json.loads(data)['all']
    relevant_points = [l for l in data if l['category']=="tracker"]
    return np.array([l['values']['frame']['time'] for l in relevant_points])

  
def find_best (reference,compared):
    def calculate_min (a):
        return  np.sqrt(((compared - a)**2).sum(axis=1)).min()
    return np.array ([calculate_min(a) for a in reference])

def eyenalysis_distance (values1, values2):
    best_1 = find_best(values1, values2)
    best_2 = find_best(values2, values1)
    norm_factor = len(values1) if len(values1) > len(values2) else len(values2)
    return (best_1.sum() + best_2.sum()) / norm_factor

file1 = "eyetribe_output.txt"
file2 = "eyetribe_output.txt"

#simple Eyenalysis distance with only (x,y) coordinates
x_y_1 = extract_x_y (file1)
x_y_2 = extract_x_y (file2)

print(eyenalysis_distance(x_y_1,x_y_2))
# TEST print(eyenalysis_distance(values1,values)) ; should be zero for sae file

#add a timestamp column
t_1 = extract_time(file1).T.reshape((len(x_y_1),1))
t_2 = extract_time(file2).T.reshape((len(x_y_2),1))
x_y_t_1 = np.concatenate((x_y_1 , t_1),axis=1)
x_y_t_2 = np.concatenate((x_y_2 , t_2),axis=1)

# "whiten" the data, remove the unit problem (milliseconds and pixels) by dividing each column by its standard deviation
norm_x_y_t_1 = whiten (x_y_t_1)
norm_x_y_t_2 = whiten (x_y_t_2)
print(eyenalysis_distance(norm_x_y_t_1,norm_x_y_t_2))

#TEST print(np.std(norm_y_y_t_1,axis=0)); should be [1,1,1]
#TEST print(eyenalysis_distance(values1,values2))  ; should be 0 for the same file

#group fixations into one row and convert the timestamp into fixation duration 
f_d_1 = extract_fix_d (x_y_t_1)
print(f_d_1)
f_d_2 = extract_fix_d (x_y_t_2)

norm_f_d_1 = whiten(f_d_1)
norm_f_d_2 = whiten(f_d_2)
print (eyenalysis_distance(norm_f_d_1,norm_f_d_2))


#values2 = np.concatenate((values2 ,  extract_time(file2).T),axis=1)


#{"category":"tracker","request":"get","statuscode":200,"values":{"frame":{"avg":{"x":0.0,"y":0.0},"fix":false,"lefteye":{"avg":{"x":3.0,"y":0.0},"pcenter":{"x":0.0,"y":0.0},"psize":0.0,"raw":{"x":0.0,"y":0.0}},"raw":{"x":0.0,"y":0.0},"righteye":{"avg":{"x":0.0,"y":0.0},"pcenter":{"x":0.0,"y":0.0},"psize":0.0,"raw":{"x":0.0,"y":0.0}},"state":16,"time":604571264,"timestamp":"2019-09-12 13:53:54.304"}}}