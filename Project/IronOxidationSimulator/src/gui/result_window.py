from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel


class ResultWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(450, 300)

        # 创建一个 QTabWidget 作为中心部件
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

    def add_result(self, title, result):
        slope, intercept, se_slope, se_intercept, r_squared = result
        result_str = (
            f"Slope: {slope}\n"
            f"Intercept: {intercept}\n"
            f"Standard error of slope: {se_slope}\n"
            f"Standard error of intercept: {se_intercept}\n"
            f"R Squared: {r_squared}"
        )

        # 创建一个新的标签页
        tab = QWidget(self.tab_widget)

        # 在标签页中添加一些内容
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel(result_str))
        tab.setLayout(layout)

        # 将标签页添加到 QTabWidget
        self.tab_widget.addTab(tab, title)
