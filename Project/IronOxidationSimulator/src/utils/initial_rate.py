import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PyQt5.QtGui import QPixmap, QImage


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
    time = np.array(time)
    conc = np.array(conc)
    conc_l, conc_h = conc[0], conc[-1]
    mask = (conc - conc_l) <= (conc_h - conc_l) * threshold
    return time[mask], conc[mask]


def plot_initial_rate(time, conc, slope, intercept, r_squared):
    fig, ax = plt.subplots(figsize=(6, 4))

    ax.scatter(time, conc, label="Data points", color="blue")
    ax.plot(time, slope * time + intercept, '-', color="red",
            label=f"Fit: y = {slope:.2f}x + {intercept:.2f}, R^2 = {r_squared:.2f}")

    ax.set_xlabel('Time')
    ax.set_ylabel('Concentration')
    ax.legend(loc="best")

    # Convert the matplotlib figure to a QPixmap
    canvas = FigureCanvas(fig)
    canvas.draw()
    width, height = fig.get_size_inches() * fig.get_dpi()
    image = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(image)

    return pixmap


def plot_rate_comparison(time, conc, slopes, r_squared_values):
    fig, ax = plt.subplots(figsize=(6, 4))

    threshold_array = np.arange(0.1, 0.51, 0.05)
    max_r2_index = np.argmax(r_squared_values)
    min_r2_index = np.argmin(r_squared_values)

    for i, slope in enumerate(slopes):
        if i == max_r2_index or i == min_r2_index:
            ax.plot(time, slope * time, label=f"Threshold: {threshold_array[i]:.2f}, R^2 = {r_squared_values[i]:.2f}")
        else:
            ax.plot(time, slope * time, alpha=0.5)  # Use lower alpha for other lines

    ax.scatter(time, conc, label="Data points", color="blue")
    ax.legend(loc="best")
    ax.set_xlabel('Time')
    ax.set_ylabel('Concentration')

    # Convert the matplotlib figure to a QPixmap
    canvas = FigureCanvas(fig)
    canvas.draw()
    width, height = fig.get_size_inches() * fig.get_dpi()
    image = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(image)

    return pixmap