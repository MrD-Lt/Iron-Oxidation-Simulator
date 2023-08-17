"""
plane3D_plot.py
----------------------
Author: Dongzi Ding
Created: 2023-08-12
Modified: 2023-08-17

This file contains functions for performing 3D plotting and regression analysis on data.
It includes functions for reading data, plotting 3D scatter points, and fitting a plane to the data.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from PyQt5.QtGui import QImage, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Plane3DPlotter:
    """
    Attributes:
        - filename (str): Name of the input Excel file containing data.
        - data (tuple): Processed data from the Excel file.
        - log_initial_concentration (array): Logged values of initial concentrations.
        - log_initial_rate (array): Logged values of initial rates.
        - pH (array): pH values from the data.
        - params (tuple): Parameters of the fitted plane.
        - r_squared (float): R-squared value of the fitted model.
    """

    def __init__(self, filename=None):
        """
        Initializes Plane3DPlotter with a given filename.

        Args:
            - filename (str, optional): Name of the input Excel file. Defaults to None.
        """
        self.filename = filename
        self.data = self.read_data(filename)
        self.log_initial_concentration, self.log_initial_rate, self.pH = (
        None, None, None) if self.data is None else self.data
        self.params = None
        self.r_squared = None

    def read_data(self, filename):
        """
        Reads data from the specified Excel file and returns logged values.

        Args:
            - filename (str): Name of the Excel file to read from.

        Returns:
            tuple: Logged initial concentration, logged initial rate, and pH values.
        """
        try:
            data = pd.read_excel(filename)
            # Assuming initial concentration is in the first column
            log_initial_concentration = np.log(data.iloc[:, 0].values)
            # Assuming initial rate is in the second column
            log_initial_rate = np.log(data.iloc[:, 1].values)
            # Assuming pH is in the third column
            pH = data.iloc[:, 2].values
            return log_initial_concentration, log_initial_rate, pH
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            return None

    def perform_analysis(self):
        """
        Performs 3D analysis on the data.

        Returns:
            tuple: Parameters of the fitted plane and R-squared value.
        """
        self.params, self.r_squared = self.fit_plane(self.log_initial_concentration, self.pH, self.log_initial_rate)
        return self.params, self.r_squared

    def fit_plane(self, log_initial_concentration, pH, log_initial_rate):
        """
        Fits a plane to the given 3D data.

        Args:
            - log_initial_concentration (array): Logged values of initial concentrations.
            - pH (array): pH values.
            - log_initial_rate (array): Logged values of initial rates.

        Returns:
            tuple: Parameters of the fitted plane and R-squared value.
        """
        X = np.column_stack((log_initial_concentration, pH))
        model = LinearRegression().fit(X, log_initial_rate)
        predictions = model.predict(X)
        r_squared = r2_score(log_initial_rate, predictions)
        return (model.intercept_, model.coef_[0], model.coef_[1]), r_squared

    def plot_3D_data(self, ax=None):
        """
        Plots the 3D data and fitted plane.

        Args:
            - ax (Axes3D, optional): Existing 3D axes if provided. Defaults to None.

        Returns:
            fig, ax: Figure and axes objects of the plot.
        """
        if self.params is None:
            self.params, _ = self.perform_analysis()
        fig, ax = self.create_3D_plot(ax)
        self.plot_fitted_plane(ax, self.params)
        return fig, ax

    def create_3D_plot(self, ax=None):
        """
        Creates a 3D plot with data points.

        Args:
            - ax (Axes3D, optional): Existing 3D axes if provided. Defaults to None.

        Returns:
            fig, ax: Figure and axes objects of the plot.
        """
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
        else:
            fig = ax.figure
        ax.scatter(self.log_initial_concentration, self.pH, self.log_initial_rate, c='k', marker='o')
        ax.set_xlabel('log(Initial Concentration)')
        ax.set_ylabel('pH')
        ax.set_zlabel('log(Initial Rate)')
        return fig, ax

    def plot_fitted_plane(self, ax, params):
        """
        Plots the fitted plane on the given 3D axes.

        Args:
            - ax (Axes3D): 3D axes object to plot on.
            - params (tuple): Parameters of the fitted plane.
        """
        log_initial_concentration_range = np.linspace(self.log_initial_concentration.min(),
                                                      self.log_initial_concentration.max(), 50)
        pH_range = np.linspace(self.pH.min(), self.pH.max(), 50)
        log_initial_concentration_grid, pH_grid = np.meshgrid(log_initial_concentration_range, pH_range)
        log_initial_rate_fit = params[0] + params[1] * log_initial_concentration_grid + params[2] * pH_grid
        ax.plot_surface(log_initial_concentration_grid, pH_grid, log_initial_rate_fit, alpha=0.5)

    def get_results(self):
        """
        Returns the parameters of the fitted plane and R-squared value.

        Returns:
            dict: Parameters of the fitted plane and R-squared value.
        """
        return {
            "params": self.params,
            "r_squared": self.r_squared
        }

    def fig_to_pixmap(self, fig):
        """
        Converts a matplotlib figure to a QPixmap.

        Args:
            - fig (Figure): Matplotlib figure to be converted.

        Returns:
            QPixmap: Converted QPixmap of the figure.
        """
        canvas = FigureCanvas(fig)
        canvas.draw()
        width, height = fig.get_size_inches() * fig.get_dpi()
        image = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(image)
        return pixmap

