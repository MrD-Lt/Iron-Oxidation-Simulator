"""
button_area.py
----------------------
Author: Dongzi Ding
Created: 2023-06-25
Modified: 2023-08-14
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QDialog, QFileDialog, \
    QTabWidget, QMessageBox

from .result_window import ResultWindow
from .visual_window import VisualWindow

from ..utils import regression_analysis, initial_rate, rate_const, plane3D_plot
from ..utils.plane3D_plot import Plane3DPlotter
from ..utils.save import save

from matplotlib.figure import Figure



class ButtonArea(QWidget):
    """
    Main button area of the application which provides the necessary buttons for the user to interact with the application.

    Attributes:
        - result: A dictionary storing the results.
        - figures: A dictionary storing the generated figures.
        - main_window: Reference to the main application window.
    """

    def __init__(self, parent=None):
        """
        Initialize the ButtonArea with necessary widgets and layouts.

        Args:
            - parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)

        self.result = {}
        self.figures = {}
        self.main_window = parent

        layout = QHBoxLayout()

        self.calculate_button = QPushButton("Start")
        self.reset_button = QPushButton("Cancel and Reset")

        self.result_button = QPushButton("Calculation Results")
        self.visual_button = QPushButton("Visualisation")
        self.save_button = QPushButton("Save Results")

        self.result_button.setEnabled(False)
        self.visual_button.setEnabled(False)
        self.save_button.setEnabled(False)

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        left_layout.addWidget(self.calculate_button)
        left_layout.addWidget(self.reset_button)
        right_layout.addWidget(self.result_button)
        right_layout.addWidget(self.visual_button)
        right_layout.addWidget(self.save_button)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.setLayout(layout)

        self.calculate_button.clicked.connect(self.calculate)
        self.reset_button.clicked.connect(self.reset)
        self.result_button.clicked.connect(self.show_result)
        self.visual_button.clicked.connect(self.show_visual)
        self.save_button.clicked.connect(self.save_result)

    def calculate(self):
        """
        Calculate functionality of the application.
        """
        if not self.main_window.input_window.data:
            QMessageBox.critical(self, "Error", "No data loaded.", QMessageBox.Ok)
            return

        selected_features = []
        for option, selected in self.main_window.settings.func_current_options.items():
            if selected:
                selected_features.append(option)

        dialog = OptionDialog(selected_features, self)
        if not dialog.exec():
            return

        for option, selected in self.main_window.settings.func_current_options.items():
            if selected:
                if option == "reaction order analysis":
                    options = dialog.get_options("reaction order analysis")
                    use_sklearn = options.get("use_sklearn", False)
                    use_both = options.get("use_both", False)

                    data = self.main_window.input_window.data[option]
                    if data is None:
                        print("No data available")
                        return
                    try:
                        x, y, sdx_absolute, sdx_upper, sdx_lower, sdy_absolute, sdy_upper, sdy_lower = data.values()
                    except:
                        try:
                            x, y, sdx_absolute, sdx_upper, sdx_lower, sdy_absolute, sdy_upper, sdy_lower = data
                        except ValueError:
                            print("Invalid data format")
                            return
                    if use_both:
                        slope_sklearn, intercept_sklearn, se_slope_sklearn, se_intercept_sklearn, r_squared_sklearn = regression_analysis.calculate_regression(
                            x, y, sdx_absolute, sdy_absolute, use_sklearn=True
                        )
                        slope, intercept, se_slope, se_intercept, r_squared = regression_analysis.calculate_regression(
                            x, y, sdx_absolute, sdy_absolute, use_sklearn=False
                        )
                        self.result[option] = {
                            "sklearn": (
                                x, y, sdx_lower, sdx_upper, sdy_lower, sdy_upper, slope_sklearn, intercept_sklearn,
                                se_slope_sklearn, se_intercept_sklearn, r_squared_sklearn),
                            "no_sklearn": (
                                x, y, sdx_lower, sdx_upper, sdy_lower, sdy_upper, slope, intercept, se_slope,
                                se_intercept,
                                r_squared)
                        }
                    else:
                        slope, intercept, se_slope, se_intercept, r_squared = regression_analysis.calculate_regression(
                            x, y, sdx_absolute, sdy_absolute, use_sklearn=use_sklearn
                        )
                        self.result[option] = {
                            "sklearn" if use_sklearn else "no_sklearn": (
                                x, y, sdx_lower, sdx_upper, sdy_lower, sdy_upper, slope, intercept, se_slope,
                                se_intercept,
                                r_squared)
                        }
                    self.result_button.setEnabled(True)
                    self.visual_button.setEnabled(True)
                    if self.main_window.settings.save_current_option == "Yes":
                        self.save_button.setEnabled(True)

                elif option == "initial rate analysis":
                    options = dialog.get_options("initial rate analysis")
                    use_specific_threshold = options.get("Use specific threshold")
                    dont_use_specific_threshold = options.get("Use a range between 5% to 20%")
                    data = self.main_window.input_window.data[option]
                    if data is None:
                        print("No data available")
                        return

                    try:
                        time, conc, threshold = data.values()
                    except ValueError:
                        print("Invalid data format")
                        return

                    if use_specific_threshold:
                        rate_result = initial_rate.calculate_rate(time, conc, threshold)
                        self.result[option] = {"Use specific threshold": rate_result}
                    else:
                        rate_results = initial_rate.calculate_rate_compare(time, conc)
                        self.result[option] = {"Use a range between 5% to 20%": rate_results}
                    self.result_button.setEnabled(True)
                    self.visual_button.setEnabled(True)
                    if self.main_window.settings.save_current_option == "Yes":
                        self.save_button.setEnabled(True)

                elif option == "rate const analysis":
                    data = self.main_window.input_window.data[option]
                    if data is None:
                        print("No data available")
                        return

                    try:
                        time, conc = data.values()
                    except ValueError:
                        print("Invalid data format")
                        return

                    rate_result = rate_const.calculate_rate(time, conc)
                    self.result[option] = {"Default": rate_result}
                    self.result_button.setEnabled(True)
                    self.visual_button.setEnabled(True)
                    if self.main_window.settings.save_current_option == "Yes":
                        self.save_button.setEnabled(True)
                elif option == "3D plane plot":
                    data = self.main_window.input_window.data[option]
                    if data is None:
                        print("No data available")
                        return
                    try:
                        pH, deltapH, logFe, deltalogFe, logR, deltalogR = data.values()
                    except:
                        try:
                            pH, deltapH, logFe, deltalogFe, logR, deltalogR = data
                        except ValueError:
                            print("Invalid data format")
                            return
                    plane_plotter = Plane3DPlotter()
                    params, r_squared = plane_plotter.perform_analysis(pH, logFe, logR)
                    self.result[option] = {
                        "Default": (pH, logFe, logR, params, r_squared)
                    }
                    self.result_button.setEnabled(True)
                    self.visual_button.setEnabled(True)
                    if self.main_window.settings.save_current_option == "Yes":
                        self.save_button.setEnabled(True)

    def reset(self):
        """
        Reset functionality of the application.
        """
        self.result_button.setEnabled(False)
        self.visual_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.main_window.settings.reset()
        self.main_window.input_window.reset()
        self.update_start_button()

    def show_result(self):
        """
        Show result functionality of the application.
        """
        self.result_window = ResultWindow(self)

        for option, selected in self.main_window.settings.func_current_options.items():
            if selected:
                if option == "reaction order analysis":
                    for method, result in self.result[option].items():
                        self.result_window.add_result(f"Reaction Order Analysis ({method})", result[6:],
                                                      "Reaction Order Analysis")
                elif option == "initial rate analysis":
                    for method, result in self.result[option].items():
                        self.result_window.add_result(f"Initial Rate Analysis ({method})", result,
                                                      "Initial Rate Analysis")
                elif option == "rate const analysis":
                    for method, result in self.result[option].items():
                        self.result_window.add_result(f"Rate Const Analysis ({method})", result, "Rate Const Analysis")
                elif option == "3D plane plot":
                    for method, result in self.result[option].items():
                        self.result_window.add_result(f"3D Plane Plot ({method})", result, "3D Plane Plot")

        self.result_window.show()

    def show_visual(self):
        """
        Show visual functionality of the application.
        """
        colors = {'no_sklearn': 'red', 'sklearn': 'blue'}

        for option, selected in self.main_window.settings.func_current_options.items():
            if selected:
                fig = Figure()
                ax = fig.add_subplot(111)
                legend_lines = []
                pixmap = None

                if option == "reaction order analysis":
                    for method, result in self.result[option].items():
                        pixmap = regression_analysis.plot_regression(*result, ax=ax, fig=fig, label=method,
                                                                     color=colors[method])

                elif option == "initial rate analysis":

                    for method, result in self.result[option].items():

                        time = result['time']
                        conc = result['conc']

                        if method == "Use specific threshold":
                            slope = result['slope']
                            intercept = result['intercept']
                            r_squared = result['r_squared']
                            pixmap = initial_rate.plot_initial_rate(time, conc, slope, intercept, r_squared)

                        elif method == "Use a range between 5% to 20%":
                            slopes = result['slopes']
                            intercepts = result['intercepts']
                            r_squared_values = result['r_squared_values']
                            pixmap = initial_rate.plot_rate_comparison(time, conc, slopes, intercepts, r_squared_values)


                elif option == "rate const analysis":

                    for method, result in self.result[option].items():
                        time = result['time']
                        conc = result['ln_conc']
                        slope = result['slope']
                        intercept = result['intercept']
                        r_squared = result['r_squared']
                        pixmap = rate_const.plot(time, conc, slope, intercept, r_squared)


                elif option == "3D plane plot":
                    for method, result in self.result[option].items():
                        fig = Figure()

                        ax = fig.add_subplot(111, projection='3d')

                        pH, logFe, logR, params, r_squared = result

                        plane_plotter = Plane3DPlotter()
                        plane_plotter.plot_3D_data(pH, logFe, logR, ax=ax)

                        plane_plotter.plot_fitted_plane(ax, pH, logFe, params)

                        equation_str = f"logR_0 = {params[1]:.2f}pH + {params[2]:.2f}logFe_0 + {params[0]:.2f}"

                        ax.set_title(equation_str)

                        ax.text(0.02, 0.98, 0.02, s=f'R^2={r_squared:.2f}', transform=ax.transAxes,
                                verticalalignment='top')

                        pixmap = plane_plotter.fig_to_pixmap(fig)

                        self.visual_window = VisualWindow(pixmap, self)

                self.figures[option] = fig

                if pixmap is not None:
                    self.visual_window = VisualWindow(pixmap, self)
                    self.visual_window.show()
                else:
                    print("Error: No valid data found to plot.")

    def save_result(self):
        """
        Save result functionality of the application.
        """
        dirname = QFileDialog.getExistingDirectory(self, "Select directory")
        if dirname:
            save(self.result, dirname, self.figures)

    def update_start_button(self):
        func_option = self.main_window.settings.func_current_option
        input_option = self.main_window.settings.input_current_option
        print("func_option: ", func_option, "\ninput_option: ", input_option)
        if func_option is not None and input_option is not None:
            self.calculate_button.setEnabled(True)
        else:
            self.calculate_button.setEnabled(False)


class OptionDialog(QDialog):
    """
        A dialog for selecting analysis options.
    """
    def __init__(self, selected_features, parent=None):
        """
            Initialize the OptionDialog.
        """
        super().__init__(parent)

        self.setWindowTitle("Options")

        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        self.tabs = {}
        for feature in selected_features:
            if feature == "reaction order analysis":
                tab = QWidget()
                self.use_sklearn_button = QRadioButton("Use sklearn")
                self.use_sklearn_button.setChecked(True)
                self.dont_use_sklearn_button = QRadioButton("Don't use sklearn")
                self.both_button = QRadioButton("Use both")

                tab_layout = QVBoxLayout()
                tab_layout.addWidget(self.use_sklearn_button)
                tab_layout.addWidget(self.dont_use_sklearn_button)
                tab_layout.addWidget(self.both_button)
                tab.setLayout(tab_layout)

                self.tabs[feature] = {"widget": tab,
                                      "options": {"use_sklearn": self.use_sklearn_button, "use_both": self.both_button}}

            if feature == "initial rate analysis":
                tab = QWidget()
                self.use_specific_threshold = QRadioButton("Use specific threshold")
                self.use_specific_threshold.setChecked(True)
                self.dont_use_specific_threshold = QRadioButton("Use a range between 5% to 20%")

                tab_layout = QVBoxLayout()
                tab_layout.addWidget(self.use_specific_threshold)
                tab_layout.addWidget(self.dont_use_specific_threshold)
                tab.setLayout(tab_layout)

                self.tabs[feature] = {"widget": tab,
                                      "options": {"Use specific threshold": self.use_specific_threshold,
                                                  "Use a range between 5% to 20%": self.dont_use_specific_threshold}}

            if feature == "rate const analysis":
                tab = QWidget()
                self.default1 = QRadioButton("Default")
                self.default1.setChecked(True)

                tab_layout = QVBoxLayout()
                tab_layout.addWidget(self.default1)
                tab.setLayout(tab_layout)

                self.tabs[feature] = {"widget": tab,
                                      "options": {"Default": self.default1}}

            if feature == "3D plane plot":
                tab = QWidget()
                self.default2 = QRadioButton("Default")
                self.default2.setChecked(True)

                tab_layout = QVBoxLayout()
                tab_layout.addWidget(self.default2)
                tab.setLayout(tab_layout)

                self.tabs[feature] = {"widget": tab,
                                      "options": {"Default": self.default2}}

        for feature, tab in self.tabs.items():
            self.tab_widget.addTab(tab["widget"], feature)

        layout.addWidget(self.tab_widget)

        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.accept)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def get_options(self, feature):
        return {option: button.isChecked() for option, button in self.tabs[feature]["options"].items()}

    def use_sklearn(self):
        return self.use_sklearn_button.isChecked()

    def use_both(self):
        return self.both_button.isChecked()