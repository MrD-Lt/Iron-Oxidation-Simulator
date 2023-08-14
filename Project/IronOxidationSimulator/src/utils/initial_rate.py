"""
initial_rate.py
----------------------
Author: Dongzi Ding
Created: 2023-06-25
Modified: 2023-08-14
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PyQt5.QtGui import QPixmap, QImage


def read_data(filename):
    """
    Reads experimental data from an Excel file.

    Parameters:
        - filename (str): Path to the Excel file.

    Returns:
        Arrays of time and concentration values.
    """
    try:
        data = pd.read_excel(filename)
        time = data.iloc[:, 0].values
        conc = data.iloc[:, 1].values
        return time, conc
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None


def calculate_rate(time, conc, threshold):
    """
    Calculates the rate of a reaction using linear regression on a subset of data.

    Parameters:
        - time (array): Time data.
        - conc (array): Concentration data.
        - threshold (float): Percentage of data to use for regression.

    Returns:
        Dictionary containing time, concentration, slope, intercept, and R squared values.
    """
    cur_time, cur_conc = cut_data(time, conc, threshold)
    time_2d = np.array(time).reshape(-1, 1)
    cur_time = np.array(cur_time).reshape(-1, 1)
    model = LinearRegression()
    model.fit(cur_time, cur_conc)
    slope = model.coef_[0]
    intercept = model.intercept_
    r_squared = model.score(time_2d, conc)

    return {
        'time': time,
        'conc': conc,
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared
    }


def calculate_rate_compare(time, conc):
    """
    Calculates rates using different thresholds and compares the fits.

    Parameters:
        - time (array): Time data.
        - conc (array): Concentration data.

    Returns:
        Dictionary containing time, concentration, slopes, intercepts, and R squared values for each threshold.
    """
    threshold_array = np.arange(0.05, 0.2, 0.01)
    slopes, intercepts, r_squared_values = [], [], []
    time_2d = np.array(time).reshape(-1, 1)
    for threshold in threshold_array:
        cur_time, cur_conc = cut_data(time, conc, threshold)
        cur_time = np.array(cur_time).reshape(-1, 1)
        model = LinearRegression()
        model.fit(cur_time, cur_conc)
        slopes.append(model.coef_[0])
        intercepts.append(model.intercept_)
        r_squared_values.append(model.score(time_2d, conc))

    return {
        'time': time,
        'conc': conc,
        'slopes': slopes,
        'intercepts': intercepts,
        'r_squared_values': r_squared_values
    }


def cut_data(time, conc, threshold):
    """
    Filters time and concentration data based on a threshold.

    Parameters:
        - time (array): Time data.
        - conc (array): Concentration data.
        - threshold (float): Threshold value for filtering.

    Returns:
        Filtered arrays of time and concentration values.
    """
    conc = np.array(conc)
    time = np.array(time)
    conc_l, conc_h = conc[0], conc[-1]
    try:
        if conc_h > conc_l:  # 如果浓度是上升的
            mask = (conc - conc_l) <= (conc_h - conc_l) * threshold[0]
        else:  # 如果浓度是下降的
            mask = (conc_l - conc) <= (conc_l - conc_h) * threshold[0]
    except:
        if conc_h > conc_l:  # 如果浓度是上升的
            mask = (conc - conc_l) <= (conc_h - conc_l) * threshold
        else:  # 如果浓度是下降的
            mask = (conc_l - conc) <= (conc_l - conc_h) * threshold

    return time[mask], conc[mask]


def plot_initial_rate(time, conc, slope, intercept, r_squared):
    """
    Generates a plot of the initial reaction rate.

    Parameters:
        - time (array): Time data.
        - conc (array): Concentration data.
        - slope (float): Slope from linear regression.
        - intercept (float): Intercept from linear regression.
        - r_squared (float): R squared value from linear regression.

    Returns:
        A QPixmap object containing the plot.
    """
    time = np.array(time)

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.scatter(time, conc, label="Data points", color="blue")
    ax.plot(time, slope * time + intercept, '-', color="red",
            label=f"Fit: y = {slope:.2f}x + {intercept:.2f}, R^2 = {r_squared:.2f}")

    ax.set_xlabel('Time')
    ax.set_ylabel('Concentration')
    ax.legend(loc="best")

    canvas = FigureCanvas(fig)
    canvas.draw()
    width, height = fig.get_size_inches() * fig.get_dpi()
    image = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(image)

    return pixmap


def plot_rate_comparison(time, conc, slopes, intercepts, r_squared_values):
    """
    Generates a plot comparing reaction rates for different thresholds.

    Parameters:
        - time (array): Time data.
        - conc (array): Concentration data.
        - slopes (list): List of slopes from linear regressions.
        - intercepts (list): List of intercepts from linear regressions.
        - r_squared_values (list): List of R squared values from linear regressions.

    Returns:
        A QPixmap object containing the comparison plot.
    """
    time = np.array(time)

    fig, ax = plt.subplots(figsize=(6, 4))

    threshold_array = np.arange(0.05, 0.2, 0.01)
    max_r2_index = np.argmax(r_squared_values)
    min_r2_index = np.argmin(r_squared_values)

    for i, (slope, intercept) in enumerate(zip(slopes, intercepts)):
        if i == max_r2_index or i == min_r2_index:
            ax.plot(time, slope * time + intercept,
                    label=f"Threshold: {threshold_array[i]:.2f}, R^2 = {r_squared_values[i]:.2f}")
        else:
            ax.plot(time, slope * time + intercept, alpha=0.6)  # Use lower alpha for other lines

    ax.scatter(time, conc, label="Data points", color="blue")
    ax.legend(loc="best")
    ax.set_xlabel('Time')
    ax.set_ylabel('Concentration')

    canvas = FigureCanvas(fig)
    canvas.draw()
    width, height = fig.get_size_inches() * fig.get_dpi()
    image = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(image)

    return pixmap
