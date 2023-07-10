from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QDialog, QFileDialog
from src.gui.result_window import ResultWindow
from src.gui.visual_window import VisualWindow
from src.utils.regression_analysis import calculate_regression, plot_regression
from src.utils.save import save


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
                if option == "reaction_order_analysis":
                    # 打开 SklearnOptionDialog 并获取用户的选择
                    dialog = SklearnOptionDialog(self)
                    dialog.exec_()
                    use_sklearn = dialog.use_sklearn()

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
                    slope, intercept, se_slope, se_intercept, r_squared = calculate_regression(
                        x, y, sdx_absolute, sdy_absolute, use_sklearn=use_sklearn
                    )

                    # 保存结果
                    self.result[
                        option] = x, y, sdx_lower, sdx_upper, sdy_lower, sdy_upper, slope, intercept, se_slope, se_intercept, r_squared

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
                if option == "reaction_order_analysis":
                    # 创建一个 ResultWindow 实例并显示它
                    print(self.result)
                    self.result_window = ResultWindow(self.result[option][6:], self)
                    self.result_window.setWindowTitle("Result Window - Reaction Order Analysis")
                    self.result_window.show()
                elif option == "option2":
                    # 显示 option2 功能的结果...
                    pass
                # 添加其他功能的处理...

    def show_visual(self):
        # 遍历所有选中的功能
        for option, selected in self.main_window.settings.func_current_options.items():
            if selected:
                if option == "reaction_order_analysis":
                    # 先调用 plot_regression 函数获取 QPixmap 对象
                    pixmap = plot_regression(*self.result)  # plot_regression 函数需要返回一个 QPixmap 对象
                    # 创建一个 VisualWindow 实例并显示它
                    self.visual_window = VisualWindow(pixmap, self)
                    self.visual_window.show()
                elif option == "option2":
                    # 显示 option2 功能的可视化...
                    pass
                # 添加其他功能的处理...

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

        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.accept)

        layout.addWidget(self.use_sklearn_button)
        layout.addWidget(self.dont_use_sklearn_button)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def use_sklearn(self):
        return self.use_sklearn_button.isChecked()
