# regression_analysis.py
from PyQt5.QtGui import QPixmap, QImage
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def read_data(filename):
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
        print("Result！！",slope, intercept, se_slope, se_intercept, r_squared)
    return slope, intercept, se_slope, se_intercept, r_squared

def plot_regression(x, y, sdx_lower, sdx_upper, sdy_lower, sdy_upper, slope, intercept, se_slope, se_intercept,
                    r_squared):
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.errorbar(x, y, yerr=[sdy_lower, sdy_upper], xerr=[sdx_lower, sdx_upper], fmt='ko')
    ax.plot([np.min(x), np.max(x)], [slope * np.min(x) + intercept, slope * np.max(x) + intercept], 'r-')
    ax.set_xlabel('log([Fe], μM)')
    ax.set_ylabel('log(R0, μMs^-1)')
    ax.legend(['Data', 'Weighted linear regression line'], loc='northwest')
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    text_x = xlim[0] + 0.1 * (xlim[1] - xlim[0])
    text_y1 = ylim[1] - 0.1 * (ylim[1] - ylim[0])
    text_y2 = ylim[1] - 0.15 * (ylim[1] - ylim[0])
    ax.text(text_x, text_y1, f"log[R0] = ({slope:.2f}±{se_slope:.2f})log[Fe] + ({intercept:.2f}±{se_intercept:.2f})")
    ax.text(text_x, text_y2, f"R² = {r_squared:.2f}")
    canvas = FigureCanvas(fig)
    canvas.draw()
    width, height = fig.get_size_inches() * fig.get_dpi()
    image = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(image)
    return pixmap


