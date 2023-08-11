import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PyQt5.QtGui import QPixmap, QImage


def read_data(filename):
    try:
        data = pd.read_excel(filename)
        time = data.iloc[:, 0].values
        conc = data.iloc[:, 1].values
        return time, conc
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None


def calculate_rate(time, conc):
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
