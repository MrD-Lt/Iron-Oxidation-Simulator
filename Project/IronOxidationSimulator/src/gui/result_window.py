from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QTextEdit

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
                slope, intercept, r_squared = result['slope'], result['intercept'], result['r_squared']
            result_str = (
                f"Slope: {slope}\n"
                f"Intercept: {intercept}\n"
                f"R Squared: {r_squared}"
            )
        elif feature_name == "Reaction Order Analysis":
            slope, intercept, se_slope, se_intercept, r_squared = result
            result_str = (
                f"Initial rate: {slope}\n"
                f"Initial conc: {intercept}\n"
                f"Standard error of the initial rate: {se_slope}\n"
                f"Standard error of the initial conc: {se_intercept}\n"
                f"R Squared: {r_squared}"
            )
        elif feature_name == "Rate Const Analysis":
            slope, intercept, r_squared = result['slope'], result['intercept'], result['r_squared']
            result_str = (
                f"Rate constant: {slope}\n"
                f"Intercept: {intercept}\n"
                f"R Squared: {r_squared}"
            )
        elif feature_name == "3D Plane Plot":
            pH, logFe, logR, params, r_squared = result
            equation_str = f"logR_0 = {params[1]:.2f}pH + {params[2]:.2f}logFe_0 + {params[0]:.2f}"
            result_str = (
                f"Equation: {equation_str}\n"
                f"R Squared: {r_squared:.2f}"
            )
        else:
            result_str = "Invalid feature name or result format"

        # 创建一个新的标签页
        tab = QWidget(self.tab_widget)

        # 在标签页中添加 QTextEdit
        layout = QVBoxLayout(tab)
        text_edit = QTextEdit()
        text_edit.setText(result_str)
        text_edit.setReadOnly(True)  # 设置为只读，防止用户修改内容
        layout.addWidget(text_edit)
        tab.setLayout(layout)

        # 将标签页添加到 QTabWidget
        self.tab_widget.addTab(tab, title)
