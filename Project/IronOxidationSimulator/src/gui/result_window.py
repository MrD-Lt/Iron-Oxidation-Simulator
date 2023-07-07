from PyQt5.QtWidgets import QLabel, QVBoxLayout, QMainWindow, QWidget

class ResultWindow(QMainWindow):
    def __init__(self, result, parent=None):
        super().__init__(parent)
        self.setFixedSize(450, 300)

        slope, intercept, se_slope, se_intercept, r_squared = result
        result_str = (
            f"Slope: {slope}\n"
            f"Intercept: {intercept}\n"
            f"Standard error of slope: {se_slope}\n"
            f"Standard error of intercept: {se_intercept}\n"
            f"R Squared: {r_squared}"
        )
        self.result_label = QLabel(result_str)
        layout = QVBoxLayout()
        layout.addWidget(self.result_label)
        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
