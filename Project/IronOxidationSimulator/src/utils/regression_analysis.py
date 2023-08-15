"""
regression_analysis.py
----------------------
Author: Dongzi Ding
Created: 2023-06-28
Modified: 2023-08-14

This file contains functions for performing regression analysis on data. 
It includes functions for reading data, calculating LINEAR regression,
and plotting the regression line.
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
        y = data.iloc[:, 0].values
        sdy_absolute = data.iloc[:, 1].values
        sdy_upper = data.iloc[:, 2].values
        sdy_lower = data.iloc[:, 3].values
        x = data.iloc[:, 4].values
        sdx_absolute = data.iloc[:, 5].values
        sdx_upper = data.iloc[:, 6].values
        sdx_lower = data.iloc[:, 7].values
        return x, y, sdx_absolute, sdx_upper, sdx_lower, sdy_absolute, sdy_upper, sdy_lower
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None


def calculate_regression(x, y, sdx_absolute=None, sdy_absolute=None, use_sklearn=False):
    """
    Calculates the linear regression of the data.

    Args:
        - x (array-like): The x data.
        - y (array-like): The y data.
        - sdx_absolute (array-like, optional): Absolute standard deviations of the x data. Defaults to None.
        - sdy_absolute (array-like, optional): Absolute standard deviations of the y data. Defaults to None.
        - use_sklearn (bool, optional): Whether to use sklearn for the regression. Defaults to False.

    Returns:
        Slope, intercept, standard error of the slope, standard error of the intercept, and the R-squared value.
    """
    x = np.array(x)
    y = np.array(y)
    if sdx_absolute is not None:
        sdx_absolute = np.array(sdx_absolute)
    if sdy_absolute is not None:
        sdy_absolute = np.array(sdy_absolute)

    if use_sklearn:
        model = LinearRegression()
        model.fit(x.reshape(-1, 1), y)
        slope = model.coef_[0]
        intercept = model.intercept_
        se_slope, se_intercept, r_squared = None, None, model.score(x.reshape(-1, 1), y)
    else:
        x = x[:, np.newaxis]
        y = y[:, np.newaxis]
        sdx_absolute = sdx_absolute[:, np.newaxis]
        sdy_absolute = sdy_absolute[:, np.newaxis]

        w = 1 / (sdy_absolute ** 2 + sdx_absolute ** 2)
        wmx = np.sum(w * x) / np.sum(w)
        wmy = np.sum(w * y) / np.sum(w)
        covwxy = np.sum(w * (x - wmx) * (y - wmy)) / np.sum(w)
        varwx = np.sum(w * (x - wmx) ** 2) / np.sum(w)
        varwy = np.sum(w * (y - wmy) ** 2) / np.sum(w)
        slope = covwxy / varwx
        intercept = wmy - slope * wmx
        residuals = y - intercept - slope * x
        mse = np.sum(w * residuals ** 2) / np.sum(w)
        se_slope = np.sqrt(mse / varwx / (len(x) - 2))
        se_intercept = se_slope * np.sqrt(np.sum(w * x ** 2) / np.sum(w))
        r_squared = covwxy ** 2 / (varwx * varwy)
    return slope, intercept, se_slope, se_intercept, r_squared


def plot_regression(x, y, sdx_lower, sdx_upper, sdy_lower, sdy_upper, slope, intercept, se_slope, se_intercept,
                    r_squared, label, color, ax, fig):
    """
    Plots the data and the regression line.

    Args:
        - x (array-like): The x data.
        - y (array-like): The y data.
        - sdx_lower (array-like): Lower standard deviations of the x data.
        - sdx_upper (array-like): Upper standard deviations of the x data.
        - sdy_lower (array-like): Lower standard deviations of the y data.
        - sdy_upper (array-like): Upper standard deviations of the y data.
        - slope (float): Slope of the regression line.
        - intercept (float): Intercept of the regression line.
        - se_slope (float): Standard error of the slope.
        - se_intercept (float): Standard error of the intercept.
        - r_squared (float): R-squared value.
        - label (str): Label for the plot.
        - color (str): Color for the plot.
        - ax (matplotlib.axes.Axes): Axes object to draw the plot onto.
        - fig (matplotlib.figure.Figure): Figure object containing the Axes.

    Returns:
        PyQt5.QtGui.QPixmap: QPixmap representation of the plot.
    """
    ax.errorbar(x, y, yerr=[sdy_lower, sdy_upper], xerr=[sdx_lower, sdx_upper], fmt='o', color=color)
    ax.plot([np.min(x), np.max(x)], [slope * np.min(x) + intercept, slope * np.max(x) + intercept], '-', color=color)
    try:
        ax.text(0.02, 0.98 - 0.06 * len(ax.texts),
                f"{label}: log[R0] = ({slope:.2f}±{se_slope:.4f})log[Fe] + ({intercept:.2f}±{se_intercept:.4f})",
                transform=ax.transAxes, verticalalignment='top', color=color)
    except:
        ax.text(0.02, 0.98 - 0.06 * len(ax.texts),
                f"{label}: log[R0] = ({slope:.2f}±{se_slope})log[Fe] + ({intercept:.2f}±{se_intercept})",
                transform=ax.transAxes, verticalalignment='top', color=color)

    ax.set_xlabel('log([Fe], μM)')
    ax.set_ylabel('log(R0, μMs^-1)')

    canvas = FigureCanvas(fig)
    canvas.draw()
    width, height = fig.get_size_inches() * fig.get_dpi()
    image = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(image)

    return pixmap
