import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


# Plan to use the top threshold% data to do Linear regression

def read_data(filename):
    try:
        data = pd.read_excel(filename)
        time = data.iloc[:, 0].values
        conc = data.iloc[:, 1].values
        return time, conc
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None


def calculate_rate(time, conc, threshold):
    cur_time, cur_conc = cut_data(time, conc, threshold)
    model = LinearRegression()
    model.fit(cur_time, cur_conc)
    slope = model.coef_[0]
    intercept = model.intercept_
    # Here the r squared we should use all the data, not the cutted data.
    r_squared = model.score(time, conc)

    return slope, intercept, r_squared


def calculate_rate_compare(time, conc):
    threshold_array = np.arange(0.1, 0.51, 0.05)
    slope, intercept, r_squared = [], [], []
    for threshold in threshold_array:
        cur_time, cur_conc = cut_data(time, conc,threshold)
        model = LinearRegression()
        model.fit(cur_time, cur_conc)
        slope.append(model.coef_[0])
        intercept.append(model.intercept_)
        # Here the r squared we should use all the data, not the cutted data.
        r_squared.append(model.score(time, conc))

    return slope, intercept, r_squared


def cut_data(time, conc, threshold):
    time_cutted = []
    conc_cutted = []
    conc_h = conc[-1]
    conc_l = conc[0]
    index = 0
    for data_point in conc:
        if (data_point - conc_l) <= (conc_h - conc_l) * threshold:
            conc_cutted.append(data_point)
            time_cutted.append(time[index])
        index += 1
    return time_cutted, conc_cutted
