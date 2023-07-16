from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QDialog, QFileDialog
from gui.result_window import ResultWindow
from gui.visual_window import VisualWindow
from utils.regression_analysis import calculate_regression, plot_regression
from utils.save import save
from PyQt5.QtGui import QPixmap, QPainter
from matplotlib.figure import Figure



class ButtonArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.result = {}
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
    # 遍历所有选中的功能
        for option, selected in self.main_window.settings.func_current_options.items():
            if selected:
                # 根据每个功能执行相应的计算
                if option == "reaction order analysis":
                    # 打开 SklearnOptionDialog 并获取用户的选择
                    dialog = SklearnOptionDialog(self)
                    dialog.exec_()
                    use_sklearn = dialog.use_sklearn()
                    use_both = dialog.use_both()  # 获取新的选项状态

                    # 获取已经读取的数据
                    data = self.main_window.input_window.data[option]
                    if data is None:
                        print("No data available")
                        return
                    try:
                        x, y, sdx_absolute, sdx_upper, sdx_lower, sdy_absolute, sdy_upper, sdy_lower = data
                    except ValueError:
                        print("Invalid data format")
                        return
                    x, y, sdx_absolute, sdx_upper, sdx_lower, sdy_absolute, sdy_upper, sdy_lower = data

                    # 调用 regression_analysis.py 中的函数
                    if use_both:  # 如果用户选择了"Use both"
                        # 先使用sklearn进行计算
                        slope_sklearn, intercept_sklearn, se_slope_sklearn, se_intercept_sklearn, r_squared_sklearn = calculate_regression(
                            x, y, sdx_absolute, sdy_absolute, use_sklearn=True
                        )
                        # 再不使用sklearn进行计算
                        slope, intercept, se_slope, se_intercept, r_squared = calculate_regression(
                            x, y, sdx_absolute, sdy_absolute, use_sklearn=False
                        )
                        # 保存结果
                        self.result[option] = {
                            "sklearn": (x, y, sdx_lower, sdx_upper, sdy_lower, sdy_upper, slope_sklearn, intercept_sklearn, se_slope_sklearn, se_intercept_sklearn, r_squared_sklearn),
                            "no_sklearn": (x, y, sdx_lower, sdx_upper, sdy_lower, sdy_upper, slope, intercept, se_slope, se_intercept, r_squared)
                        }
                    else:
                        # 只进行一次计算
                        slope, intercept, se_slope, se_intercept, r_squared = calculate_regression(
                            x, y, sdx_absolute, sdy_absolute, use_sklearn=use_sklearn
                        )
                        # 保存结果
                        self.result[option] = {
                            "sklearn" if use_sklearn else "no_sklearn": (x, y, sdx_lower, sdx_upper, sdy_lower, sdy_upper, slope, intercept, se_slope, se_intercept, r_squared)
                        }

                    # 设置右侧部分的按钮为启用状态
                    self.result_button.setEnabled(True)
                    self.visual_button.setEnabled(True)
                    if self.main_window.settings.save_current_option == "Yes":
                        self.save_button.setEnabled(True)
                elif option == "example":
                    # 执行 "example" 的计算...
                    ...


    def reset(self):
        # 设置右侧部分的按钮为禁用状态
        self.result_button.setEnabled(False)
        self.visual_button.setEnabled(False)
        self.save_button.setEnabled(False)
        # 重置 MainWindow 中的 Settings
        self.main_window.settings.reset()
        # 重置 InputWindow
        self.main_window.input_window.reset()
        self.update_start_button()

    def show_result(self):
        # 遍历所有选中的功能
        for option, selected in self.main_window.settings.func_current_options.items():
            if selected:
                if option == "reaction order analysis":
                    # 遍历每种方法的结果
                    for method, result in self.result[option].items():
                        # 创建一个 ResultWindow 实例并显示它
                        self.result_window = ResultWindow(result[6:], self)
                        self.result_window.setWindowTitle(f"Result Window - Reaction Order Analysis ({method})")
                        self.result_window.show()
                elif option == "option2":
                    # 显示 option2 功能的结果...
                    pass
                # 添加其他功能的处理...

    def show_visual(self):
        colors = {'no_sklearn': 'red', 'sklearn': 'blue'}  # 创建一个颜色字典，键是方法的名字，值是颜色

        fig = Figure()
        ax = fig.add_subplot(111)
        legend_lines = []  # 用于保存所有图例的列表

        # 遍历所有选中的功能
        for option, selected in self.main_window.settings.func_current_options.items():
            if selected:
                if option == "reaction order analysis":
                    # 遍历每种方法的结果
                    for method, result in self.result[option].items():
                        # 调用 plot_regression 函数获取图例对象和 QPixmap 对象
                        pixmap = plot_regression(*result, ax=ax, fig=fig, label=method,
                                                              color=colors[method])  # 使用 color 参数

                elif option == "option2":
                    # 显示 option2 功能的结果...
                    pass
                # 添加其他功能的处理...

        self.visual_window = VisualWindow(pixmap, self)
        self.visual_window.show()


    def save_result(self):
        # 获取用户选择的文件路径
        filename, _ = QFileDialog.getSaveFileName(self, "Save file", "", "All Files (*)")
        if filename:
            # 保存结果和图像
            save(self.result, filename)

    def update_start_button(self):
        func_option = self.main_window.settings.func_current_option
        input_option = self.main_window.settings.input_current_option

        if func_option is not None and input_option is not None and self.main_window.input_window.data != {}:
            self.calculate_button.setEnabled(True)
        else:
            self.calculate_button.setEnabled(False)


class SklearnOptionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.use_sklearn_button = QRadioButton("Use sklearn")
        self.dont_use_sklearn_button = QRadioButton("Don't use sklearn")
        self.both_button = QRadioButton("Use both")  # 新增选项

        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.accept)

        layout.addWidget(self.use_sklearn_button)
        layout.addWidget(self.dont_use_sklearn_button)
        layout.addWidget(self.both_button)  # 新增选项
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def use_sklearn(self):
        return self.use_sklearn_button.isChecked()

    def use_both(self):  # 新增函数
        return self.both_button.isChecked()

