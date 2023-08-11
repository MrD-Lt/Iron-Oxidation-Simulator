from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel


class ResultWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(450, 300)

        # 创建一个 QTabWidget 作为中心部件
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

    def add_result(self, title, result, feature_name):
        if feature_name == "Initial Rate Analysis":
            try:
                slope, intercept, r_squared = result['slopes'], result['intercepts'], result['r_squared_values']
            except:
                slope, intercept, r_squared = result['slope'],result['intercept'],result['r_squared']
            result_str = (
                f"Slope: {slope}\n"
                f"Intercept: {intercept}\n"
                f"R Squared: {r_squared}"
            )
        elif feature_name == "Reaction Order Analysis":
            slope, intercept, se_slope, se_intercept, r_squared = result
            result_str = (
                f"initial rate: {slope}\n"
                f"initial conc: {intercept}\n"
                f"Standard error of the initial rate: {se_slope}\n"
                f"Standard error of the initial conc: {se_intercept}\n"
                f"R Squared: {r_squared}"
            )
        elif feature_name == "Rate Const Analysis":
            slope, intercept, r_squared = result['slope'], result['intercept'],result['r_squared']
            result_str = (
                f"rate constant: {slope}\n"
                f"Intercept: {intercept}\n"
                f"R Squared: {r_squared}"
            )

        else:
            result_str = "Invalid feature name or result format"

        # 创建一个新的标签页
        tab = QWidget(self.tab_widget)

        # 在标签页中添加一些内容
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel(result_str))
        tab.setLayout(layout)

        # 将标签页添加到 QTabWidget
        self.tab_widget.addTab(tab, title)

