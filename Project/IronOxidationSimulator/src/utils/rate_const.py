"""
rate_const.py
----------------------
Author: Dongzi Ding
Created: 2023-08-10
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
    Reads data from the given filename.

    Args:
        - filename (str): Path to the data file.

    Returns:
        Time and concentration values or None if an error occurs.
    """
    try:
        data = pd.read_excel(filename)
        time = data.iloc[:, 0].values
        conc = data.iloc[:, 1].values
        return time, conc
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None


def calculate_rate(time, conc):
    """
    Calculates the reaction rate using regression on logarithmic concentration.

    Args:
        - time (array-like): Array of time values.
        - conc (array-like): Array of concentration values.

    Returns:
        Calculated values including time, logarithmic concentration, slope, intercept, and R squared value.
    """
    conc = np.log(conc)

    time_2d = np.array(time).reshape(-1, 1)
    cur_time = np.array(time).reshape(-1, 1)
    model = LinearRegression()
    model.fit(cur_time, conc)
    slope = model.coef_[0]
    intercept = model.intercept_
    r_squared = model.score(time_2d, conc)

    return {
        'time': time,
        'ln_conc': conc,
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared
    }


def plot(time, conc, slope, intercept, r_squared):
    """
    Plots the given time and logarithmic concentration data with a linear fit.

    Args:
        - time (array-like): Array of time values.
        - conc (array-like): Array of logarithmic concentration values.
        - slope (float): Slope from linear regression.
        - intercept (float): Intercept from linear regression.
        - r_squared (float): R squared value from linear regression.

    Returns:
        PyQt5.QtGui.QPixmap: Pixmap representation of the plot.
    """
    time = np.array(time)

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.scatter(time, conc, label="Data points", color="blue")
    ax.plot(time, slope * time + intercept, '-', color="red",
            label=f"Fit: y = {slope:.2f}x + {intercept:.2f}, R^2 = {r_squared:.2f}")

    ax.set_xlabel('Time')
    ax.set_ylabel('ln_Concentration')
    ax.legend(loc="best")

    # Convert the matplotlib figure to a QPixmap
    canvas = FigureCanvas(fig)
    canvas.draw()
    width, height = fig.get_size_inches() * fig.get_dpi()
    image = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(image)

    return pixmap
