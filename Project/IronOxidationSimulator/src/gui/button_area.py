from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton


class ButtonArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

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
        # TODO: 开始计算
        # 设置右侧部分的按钮为启用状态
        self.result_button.setEnabled(True)
        self.visual_button.setEnabled(True)
        if self.main_window.settings.save_current_option == "Yes":
            self.save_button.setEnabled(True)

    def reset(self):
        # TODO: 取消并重置
        # 设置右侧部分的按钮为禁用状态
        self.result_button.setEnabled(False)
        self.visual_button.setEnabled(False)
        self.save_button.setEnabled(False)
        # 重置 MainWindow 中的 Settings
        self.main_window.settings.reset()

    def show_result(self):
        # TODO: 打开计算结果窗口
        pass

    def show_visual(self):
        # TODO: 打开可视化展示窗口
        pass

    def save_result(self):
        # TODO: 保存结果
        pass
