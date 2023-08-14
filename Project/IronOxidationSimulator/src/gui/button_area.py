from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QDialog, QFileDialog, \
    QTabWidget, QMessageBox
from gui.result_window import ResultWindow
from gui.visual_window import VisualWindow
from utils import regression_analysis, initial_rate, rate_const, plane3D_plot
from utils.plane3D_plot import Plane3DPlotter
from utils.save import save
from matplotlib.figure import Figure


class ButtonArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.result = {}
        self.figures = {}
        self.main_window = parent

        layout = QHBoxLayout()

        # 创建左侧部分的按钮
        self.calculate_button = QPushButton("Start")
        self.reset_button = QPushButton("Cancel and Reset")

        # 创建右侧部分的按钮
        self.result_button = QPushButton("Calculation Results")
        self.visual_button = QPushButton("Visualisation")
        self.save_button = QPushButton("Save Results")

        # 设置右侧部分的按钮为禁用状态
        self.result_button.setEnabled(False)
        self.visual_button.setEnabled(False)
        self.save_button.setEnabled(False)

        # 创建左侧和右侧的布局
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # 添加按钮到左侧和右侧的布局
        left_layout.addWidget(self.calculate_button)
        left_layout.addWidget(self.reset_button)
        right_layout.addWidget(self.result_button)
        right_layout.addWidget(self.visual_button)
        right_layout.addWidget(self.save_button)

        # 添加左侧和右侧的布局到主布局
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.setLayout(layout)

        # 连接按钮点击事件
        self.calculate_button.clicked.connect(self.calculate)
        self.reset_button.clicked.connect(self.reset)
        self.result_button.clicked.connect(self.show_result)
        self.visual_button.clicked.connect(self.show_visual)
        self.save_button.clicked.connect(self.save_result)

    def calculate(self):
        # 执行计算前先判断是否有数据
        if not self.main_window.input_window.data:
            QMessageBox.critical(self, "Error", "No data loaded.", QMessageBox.Ok)
            return

        # 创建一个空列表来收集选中的功能
        selected_features = []
        for option, selected in self.main_window.settings.func_current_options.items():
            if selected:
                selected_features.append(option)

        # 创建 OptionDialog 对象，将选中的功能列表作为参数传递
        dialog = OptionDialog(selected_features, self)
        if not dialog.exec():
            return  # 用户点击了取消，所以我们不做任何事情

        # 遍历所有选中的功能
        for option, selected in self.main_window.settings.func_current_options.items():
            if selected:
                # 根据每个功能执行相应的计算
                if option == "reaction order analysis":
                    # 从 dialog 对象中获取功能的选项状态
                    options = dialog.get_options("reaction order analysis")
                    use_sklearn = options.get("use_sklearn", False)
                    use_both = options.get("use_both", False)

                    # 获取已经读取的数据
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

                    # 调用 regression_analysis.py 中的函数
                    if use_both:  # 如果用户选择了"Use both"
                        # 先使用sklearn进行计算
                        slope_sklearn, intercept_sklearn, se_slope_sklearn, se_intercept_sklearn, r_squared_sklearn = regression_analysis.calculate_regression(
                            x, y, sdx_absolute, sdy_absolute, use_sklearn=True
                        )
                        # 再不使用sklearn进行计算
                        slope, intercept, se_slope, se_intercept, r_squared = regression_analysis.calculate_regression(
                            x, y, sdx_absolute, sdy_absolute, use_sklearn=False
                        )
                        # 保存结果
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
                        # 只进行一次计算
                        slope, intercept, se_slope, se_intercept, r_squared = regression_analysis.calculate_regression(
                            x, y, sdx_absolute, sdy_absolute, use_sklearn=use_sklearn
                        )
                        # 保存结果
                        self.result[option] = {
                            "sklearn" if use_sklearn else "no_sklearn": (
                                x, y, sdx_lower, sdx_upper, sdy_lower, sdy_upper, slope, intercept, se_slope,
                                se_intercept,
                                r_squared)
                        }

                    # 设置右侧部分的按钮为启用状态
                    self.result_button.setEnabled(True)
                    self.visual_button.setEnabled(True)
                    if self.main_window.settings.save_current_option == "Yes":
                        self.save_button.setEnabled(True)

                elif option == "initial rate analysis":
                    # 从 dialog 对象中获取功能的选项状态
                    options = dialog.get_options("initial rate analysis")
                    use_specific_threshold = options.get("Use specific threshold")
                    dont_use_specific_threshold = options.get("Use a range between 5% to 20%")

                    # 获取已经读取的数据
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

                    # 设置右侧部分的按钮为启用状态
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

                    # 设置右侧部分的按钮为启用状态
                    self.result_button.setEnabled(True)
                    self.visual_button.setEnabled(True)
                    if self.main_window.settings.save_current_option == "Yes":
                        self.save_button.setEnabled(True)
                elif option == "3D plane plot":
                    # 获取已经读取的数据
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

                    # 调用 plane3D_plot.py 中的函数
                    plane_plotter = Plane3DPlotter()  # 创建实例
                    params, r_squared = plane_plotter.perform_analysis(pH, logFe, logR)
                    # 保存结果
                    self.result[option] = {
                        "Default": (pH, logFe, logR, params, r_squared)
                    }

                    # 设置右侧部分的按钮为启用状态
                    self.result_button.setEnabled(True)
                    self.visual_button.setEnabled(True)
                    if self.main_window.settings.save_current_option == "Yes":
                        self.save_button.setEnabled(True)

    def reset(self):
        self.result_button.setEnabled(False)
        self.visual_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.main_window.settings.reset()
        self.main_window.input_window.reset()
        self.update_start_button()

    def show_result(self):
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
        colors = {'no_sklearn': 'red', 'sklearn': 'blue'}

        for option, selected in self.main_window.settings.func_current_options.items():
            if selected:
                fig = Figure()  # 创建一个新的 Figure 对象
                ax = fig.add_subplot(111)
                legend_lines = []  # 用于保存所有图例的列表
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
                        fig = Figure()  # 创建一个新的 Figure 对象

                        ax = fig.add_subplot(111, projection='3d')

                        # 从结果中解压数据

                        pH, logFe, logR, params, r_squared = result

                        plane_plotter = Plane3DPlotter()
                        plane_plotter.plot_3D_data(pH, logFe, logR, ax=ax)  # 创建3D散点图

                        plane_plotter.plot_fitted_plane(ax, pH, logFe, params)  # 添加拟合的平面

                        # 显示方程和R^2值

                        equation_str = f"logR_0 = {params[1]:.2f}pH + {params[2]:.2f}logFe_0 + {params[0]:.2f}"

                        ax.set_title(equation_str)

                        ax.text(0.02, 0.98, 0.02, s=f'R^2={r_squared:.2f}', transform=ax.transAxes, verticalalignment='top')


                        pixmap = plane_plotter.fig_to_pixmap(fig)  # 转换Figure为QPixmap

                        self.visual_window = VisualWindow(pixmap, self)


                self.figures[option] = fig  # 保存 Figure 对象

                if pixmap is not None:
                    self.visual_window = VisualWindow(pixmap, self)
                    self.visual_window.show()
                else:
                    print("Error: No valid data found to plot.")

    def save_result(self):
        dirname = QFileDialog.getExistingDirectory(self, "Select directory")
        if dirname:
            save(self.result, dirname, self.figures)  # 修改为 self.figures

    def update_start_button(self):
        func_option = self.main_window.settings.func_current_option
        input_option = self.main_window.settings.input_current_option
        print("func_option: ", func_option, "\ninput_option: ", input_option)
        if func_option is not None and input_option is not None:
            self.calculate_button.setEnabled(True)
        else:
            self.calculate_button.setEnabled(False)

class OptionDialog(QDialog):
    def __init__(self, selected_features, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Options")

        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        self.tabs = {}
        for feature in selected_features:
            if feature == "reaction order analysis":
                # 创建 Reaction Order Analysis 选项对话框并添加到标签页
                tab = QWidget()
                self.use_sklearn_button = QRadioButton("Use sklearn")
                self.use_sklearn_button.setChecked(True)  # 设置为默认选项
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
                self.use_specific_threshold.setChecked(True)  # 设置为默认选项
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
                self.default1.setChecked(True)  # 设置为默认选项

                tab_layout = QVBoxLayout()
                tab_layout.addWidget(self.default1)
                tab.setLayout(tab_layout)

                self.tabs[feature] = {"widget": tab,
                                      "options": {"Default": self.default1}}

            if feature == "3D plane plot":
                tab = QWidget()
                self.default2 = QRadioButton("Default")
                self.default2.setChecked(True)  # 设置为默认选项

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

    def use_both(self):  # 新增函数
        return self.both_button.isChecked()
