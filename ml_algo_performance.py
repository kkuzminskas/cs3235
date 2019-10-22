import sklearn
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import ShuffleSplit
from sklearn.pipeline import Pipeline
import sklearn.feature_selection as fs
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import sklearn.metrics as met
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
import prep_data.py

import warnings
# This is here to stop the warning for precision that says it is 0 if there are no predicted values for a class
warnings.filterwarnings("ignore")


## Should use bootstrap b/c it is better for a smaller sample size
## Split data
num_splits = 2#pd_data.shape[0]
bs_indices = ShuffleSplit(num_splits, random_state=0, test_size=0.2)

num_features = 6
# chi2 only works w/ non-negative values, use anova
feat_anova = fs.SelectKBest(fs.f_classif, k=num_features)
algos = [KNeighborsClassifier(), SVC(), GaussianNB(), DecisionTreeClassifier()]
algo_names = ["KNN", "SVM", "GNB", "DTC"]


performance = {'accuracy': {},
                'precision_list': {},
                'precision_avg': {}}
                
for algo in algo_names:
    performance['accuracy'][algo] = 0
    performance['precision_list'][algo] = np.zeros((1, len(np.unique(y))))
    performance['precision_avg'][algo] = 0

for train_ind, test_ind  in bs_indices.split(np_data):
    # Get the training and test data sets
    x_train = np_data[train_ind]
    y_train = y[train_ind]
    x_test = np_data[test_ind]
    y_test = y[test_ind]

    # TODO: Hyperparameter tuning for the algorithms
    # TODO: Feature selection tuning (i.e. number of selected features)

    # Feature selection and train each algorithm
    for index, algo in enumerate(algos):
        algo_name = algo_names[index]

        clf = Pipeline([('feature_selection', feat_anova),
                    ('algo', algo)])

        clf.fit(x_train, y_train)
        preds = clf.predict(x_test)

        # evaluating the performance of the algorithm
        accuracy = met.accuracy_score(y_test, preds)
        precision_list = np.array(met.precision_score(y_test, preds, average=None))
        precision_avg = met.precision_score(y_test, preds, average='weighted')

        performance['accuracy'][algo_name] += accuracy/num_splits
        performance['precision_list'][algo_name] += precision_list/num_splits
        performance['precision_avg'][algo_name] += precision_avg/num_splits


print(pd.DataFrame(performance)[['accuracy', 'precision_avg']])
