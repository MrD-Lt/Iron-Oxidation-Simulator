"""
visual_window.py
----------------------
Author: Dongzi Ding
Created: 2023-07-01
Modified: 2023-08-14
"""

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QMainWindow, QWidget
from PyQt5 import QtCore


class VisualWindow(QMainWindow):
    """
    A QMainWindow class to display an image in a window for visualization purposes.

    Attributes:
        - image_label (QLabel): A label widget to display the image.
        - central_widget (QWidget): The central widget containing the image label.
    """

    def __init__(self, pixmap, parent=None):
        """
        Initializes the VisualWindow with a QPixmap to display and an optional parent widget.

        Args:
            - pixmap (QPixmap): The image to be displayed.
            - parent (QWidget, optional): The parent widget of the VisualWindow. Defaults to None.
        """
        super().__init__(parent)
        self.setWindowTitle("Visualisation")

        self.image_label = QLabel()
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(),
                                                 aspectRatioMode=QtCore.Qt.KeepAspectRatio))

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
