"""
plane3D_plot.py
----------------------
Author: Dongzi Ding
Created: 2023-08-12
Modified: 2023-08-14

This file contains functions for performing 3D plotting and regression analysis on data.
It includes functions for reading data, plotting 3D scatter points, and fitting a plane to the data.
"""

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PyQt5.QtGui import QPixmap, QImage




class Plane3DPlotter:
    """
    A class for performing 3D plotting and regression analysis on data.

    Attributes:
        - filename (str): The path to the data file.
        - data (tuple): Data values for pH, deltapH, logFe, deltalogFe, logR, deltalogR.
        - params (tuple): Regression parameters.
        - r_squared (float): R squared value of regression analysis.

    Methods:
        - read_data: Read data from a file.
        - perform_analysis: Perform regression analysis.
        - fit_plane: Fit a plane to the data.
        - plot_3D_data: Plot the 3D data with a fitted plane.
        - create_3D_plot: Create a 3D plot.
        - plot_fitted_plane: Plot a fitted plane on 3D data.
        - get_results: Retrieve analysis results.
        - fig_to_pixmap: Convert a Matplotlib figure to a QPixmap.
    """
    def __init__(self, filename=None):
        """
        Initializes the Plane3DPlotter object.

        Args:
            - filename (str, optional): Path to the data file. Defaults to None.
        """
        self.filename = filename
        self.data = self.read_data(filename)
        self.params = None
        self.r_squared = None
        if self.data:
            self.pH, self.deltapH, self.logFe, self.deltalogFe, self.logR, self.deltalogR = self.data

    def read_data(self, filename):
        """
        Reads data from a file.

        Args:
            - filename (str): Path to the data file.

        Returns:
            Data values for pH, deltapH, logFe, deltalogFe, logR, deltalogR or None if an error occurs.
        """
        try:
            data = pd.read_excel(filename)
            pH = data.iloc[:, 1].values
            deltapH = data.iloc[:, 2].values
            logFe = data.iloc[:, 7].values
            deltalogFe = data.iloc[:, 8].values
            logR = data.iloc[:, 9].values
            deltalogR = data.iloc[:, 10].values
            return pH, deltapH, logFe, deltalogFe, logR, deltalogR
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            return None

    def perform_analysis(self, pH, logFe, logR):
        """
        Perform regression analysis on data.

        Args:
            - pH (array-like): pH values.
            - logFe (array-like): logFe values.
            - logR (array-like): logR values.

        Returns:
            Regression parameters and R squared value.
        """
        self.params, self.r_squared = self.fit_plane(pH, logFe, logR)
        return self.params, self.r_squared

    def fit_plane(self, pH, logFe, logR):
        """
        Fits a plane to the data.

        Args:
            - pH (array-like): pH values.
            - logFe (array-like): logFe values.
            - logR (array-like): logR values.

        Returns:
            Regression parameters and R squared value.
        """
        X = np.column_stack((pH, logFe))
        model = LinearRegression().fit(X, logR)
        predictions = model.predict(X)
        r_squared = r2_score(logR, predictions)
        return (model.intercept_, model.coef_[0], model.coef_[1]), r_squared

    def plot_3D_data(self, pH, logFe, logR, ax=None):
        """
        Plot the 3D data along with the fitted plane.

        Args:
            - pH (array-like): pH values.
            - logFe (array-like): logFe values.
            - logR (array-like): logR values.
            - ax (matplotlib.axes._subplots.Axes3DSubplot, optional): 3D subplot. Defaults to None.

        Returns:
            Matplotlib figure and 3D subplot.
        """
        if self.params is None:
            self.params, _ = self.perform_analysis(pH, logFe, logR)
        if pH is None:
            pH = self.pH
        if logFe is None:
            logFe = self.logFe
        if logR is None:
            logR = self.logR
        fig, ax = self.create_3D_plot(pH, logFe, logR, ax)
        self.plot_fitted_plane(ax, pH, logFe, self.params)
        return fig, ax

    def create_3D_plot(self, pH, logFe, logR, ax=None):
        """
        Creates a 3D plot for the given data.

        Args:
            - pH (array-like): pH values.
            - logFe (array-like): logFe values.
            - logR (array-like): logR values.
            - ax (matplotlib.axes._subplots.Axes3DSubplot, optional): 3D subplot. Defaults to None.

        Returns:
            Matplotlib figure and 3D subplot.
        """
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
        else:
            fig = ax.figure  # 获取ax所属的figure对象
        ax.scatter(pH, logFe, logR, c='k', marker='o')
        ax.set_xlabel('pH')
        ax.set_ylabel('logFe_0')
        ax.set_zlabel('logR_0')
        return fig, ax

    def plot_fitted_plane(self, ax, pH, logFe, params):
        """
        Plots a fitted plane on the 3D data.

        Args:
            - ax (matplotlib.axes._subplots.Axes3DSubplot): 3D subplot.
            - pH (array-like): pH values.
            - logFe (array-like): logFe values.
            - params (tuple): Regression parameters.

        Returns:
            PyQt5.QtGui.QPixmap: Pixmap representation of the plot.
        """
        pH = np.array(pH)
        logFe = np.array(logFe)
        pH_range = np.linspace(pH.min(), pH.max(), 50)
        logFe_range = np.linspace(logFe.min(), logFe.max(), 50)
        pH_grid, logFe_grid = np.meshgrid(pH_range, logFe_range)
        logR_fit = params[0] + params[1] * pH_grid + params[2] * logFe_grid
        ax.plot_surface(pH_grid, logFe_grid, logR_fit, alpha=0.5)
        canvas = FigureCanvas(ax.figure)
        canvas.draw()
        width, height = ax.figure.get_size_inches() * ax.figure.get_dpi()
        image = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(image)
        return pixmap

    def get_results(self):
        """
        Retrieve the regression analysis results.

        Returns:
            dict: Regression parameters and R squared value.
        """
        return {
            "params": self.params,
            "r_squared": self.r_squared
        }

    def fig_to_pixmap(self,fig):
        """
        Converts a Matplotlib figure to a QPixmap.

        Args:
            - fig (matplotlib.figure.Figure): Matplotlib figure.

        Returns:
            PyQt5.QtGui.QPixmap: Pixmap representation of the figure.
        """
        canvas = FigureCanvas(fig)
        canvas.draw()
        width, height = fig.get_size_inches() * fig.get_dpi()
        image = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(image)
        return pixmap