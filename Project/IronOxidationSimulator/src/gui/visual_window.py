from PyQt5.QtWidgets import QLabel, QVBoxLayout, QMainWindow, QWidget
from PyQt5 import QtCore

class VisualWindow(QMainWindow):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Visualisation")
        

        self.image_label = QLabel()
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio))

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        
        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
