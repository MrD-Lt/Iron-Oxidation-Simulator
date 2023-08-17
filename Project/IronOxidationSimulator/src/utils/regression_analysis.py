"""
regression_analysis.py
----------------------
Author: Dongzi Ding
Created: 2023-06-28
Modified: 2023-08-17
"""

from PyQt5.QtGui import QPixmap, QImage
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def read_data(filename):
    """
    Reads data from an Excel file.

    Args:
        - filename (str): Path to the Excel file.

    Returns:
        Data extracted from the file or None if an error occurs.
    """
    try:
        data = pd.read_excel(filename)
        initial_concentration = data.iloc[:, 0].values
        initial_rate = data.iloc[:, 1].values
        return initial_concentration, initial_rate
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None


def calculate_log_values(initial_concentration, initial_rate):
    """
    Calculates the log values of the initial concentration and rate.

    Args:
        - initial_concentration (array-like): Initial concentrations.
        - initial_rate (array-like): Initial rates.

    Returns:
        Log values of the initial concentration and rate.
    """
    return np.log(initial_concentration), np.log(initial_rate)


def calculate_regression(log_concentration, log_rate):
    """
    Calculates the linear regression of the log values using sklearn.

    Args:
        - log_concentration (array-like): The log concentration data.
        - log_rate (array-like): The log rate data.

    Returns:
        Slope (reaction order), intercept, and the R-squared value.
    """
    model = LinearRegression()
    model.fit(log_concentration.reshape(-1, 1), log_rate)
    slope = model.coef_[0]
    intercept = model.intercept_
    r_squared = model.score(log_concentration.reshape(-1, 1), log_rate)
    return slope, intercept, r_squared


def plot_regression(log_concentration, log_rate, slope, intercept, r_squared, label, color, ax, fig):
    """
    Plots the data and the regression line.

    Args:
        - log_concentration (array-like): The log concentration data.
        - log_rate (array-like): The log rate data.
        - slope (float): Slope of the regression line.
        - intercept (float): Intercept of the regression line.
        - r_squared (float): R-squared value.
        - label (str): Label for the plot.
        - color (str): Color for the plot.
        - ax (matplotlib.axes.Axes): Axes object to draw the plot onto.
        - fig (matplotlib.figure.Figure): Figure object containing the Axes.

    Returns:
        PyQt5.QtGui.QPixmap: QPixmap representation of the plot.
    """
    ax.plot(log_concentration, log_rate, 'o', color=color)
    ax.plot([np.min(log_concentration), np.max(log_concentration)],
            [slope * np.min(log_concentration) + intercept, slope * np.max(log_concentration) + intercept],
            '-', color=color)
    ax.text(0.02, 0.98,
            f"{label}: log[R0] = ({slope:.2f})log[X] + ({intercept:.2f})",
            transform=ax.transAxes, verticalalignment='top', color=color)

    ax.set_xlabel('log([X], μM)')
    ax.set_ylabel('log(R0, μMs^-1)')

    canvas = FigureCanvas(fig)
    canvas.draw()
    width, height = fig.get_size_inches() * fig.get_dpi()
    image = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(image)

    return pixmap
