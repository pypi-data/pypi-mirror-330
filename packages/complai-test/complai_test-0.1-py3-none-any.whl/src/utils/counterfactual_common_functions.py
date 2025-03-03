import math
import pandas as pd
import numpy as np
from collections import Counter


def rowFun(row):
    return row.name

def nearest_real_counterfactual(x_data, index, y_pred_label,distance_method,x_mad=None):
    '''
    Function to find nearest counterfactual datapoint of a chosen index and given distance method and counterfactual's index
    Implemented from Paper: Google What If Tool IEEE System Paper (https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8807255)
    '''
    try:
        INTMAX = 100000000000
        x_dataset = x_data
        x_data = x_data.to_numpy()

        if distance_method=="l1":
            x_data_std = x_mad  # Columnwise Standard deviation
        else:
            x_data_std = np.std(x_data, axis=0)
        # Selected Datapoint
        datapoint = x_data[index]

        label = y_pred_label.iloc[index]

        idx_list = [item[0] for item in np.argwhere(y_pred_label.values != label)]
        # Finding Neartes Counterfactual
        counterfactual_idx = INTMAX
        min_distance_val = INTMAX
        dist_val = 0
        for i in idx_list:
            dist_val = distance(datapoint, x_data[i], x_data_std, distance_method)
            if (dist_val < min_distance_val):
                min_distance_val = dist_val
                counterfactual_idx = i
        counterfact = dict(x_dataset.iloc[counterfactual_idx])
        new_list = []
        new_list.append(counterfact)
        counterfact = pd.DataFrame(data=new_list)
        counterfact_dict = counterfact.to_dict(orient='records')

        return counterfact_dict[0]
    except IndexError:
        return {}

def distance(x, y, std_dev, method="l1"):
    '''
    Function to calculate distance between two datapoints.
    method = l1: Manhattan Distance
           = l2: Euclidean Distance
    '''
    #try:
    y = y.reshape(x.shape)
    if method == 'l1':
        dist_val = 0
        for i in range(x.shape[0]):
            try:
                dist_val += abs(x[i] - y[i]) / std_dev[i]
            except TypeError:
                dist_val += 0.0 if x[i] ==y[i] else 1.0
            except KeyError:
                pass
        return dist_val
    elif method == 'l2':
        dist_val = 0
        for i in range(x.shape[0]):
            dist_val += ((x[i] - y[i]) ** 2) / std_dev[i]
        return math.sqrt(dist_val)
    # except TypeError:
    #     return 0.0


def get_robustness_score(ins, cf_np, x_data_std, dist_method="l1"):
    '''
    Function to calculate the overall robustness score on the passed model based on counterfactual methods (CERScore) from Certifai.
    Note: Individual distance will be saturated to 1 if distance is greater than 1.25
    Args:
        model (sklearn model): Pretrained Model for Robustness Calculation
        x_train (pandas dataframe): Training Dataset for synthetic counterfact finding
        y_train (pandas dataframe): Training Labels corresponding to Training Dataset
        x_val (pandas dataframe): For the dataset we want to generate report (usually validation dataset)
        cf_method (string): Synthetic Counterfactual Finding Method (usually same as create_explanation_report function call)
        dist_method (string): How to calculate distance of real datapoint and their corresponding synthetic counterfacts. Options are ['l1','l2']
        threshold (float): Threshold for counterfactual
    Returns:
        robustness (float): Final Robustness Score
    '''

    cf_np = cf_np.apply(pd.Series)

    dist_val = distance(ins.values,
                             cf_np.values, x_data_std,
                             dist_method)


    if dist_val >= 1:
        dist_val = 1

    return dist_val


def get_feature_change(instance=None, dictionary=None):
    try:
        instance_dict = instance.to_dict()
        cf_dict = dictionary.to_dict()["nearest_synthetic_counterfactual_sparsity"]
        diff_dict = {}
        for k in instance_dict.keys():
            v1, v2 = tuple(d[k] for d in [instance_dict, cf_dict])
            if v1 != v2:
                diff_dict[k] = (v1, v2)
        return Counter(diff_dict.keys())
    except TypeError:
        return 0