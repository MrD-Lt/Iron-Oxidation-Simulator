from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap


class VisualWindow(QWidget):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        # 创建 QLabel 来展示图像
        self.image_label = QLabel()
        self.image_label.setPixmap(pixmap)
        # 创建 QVBoxLayout 并添加 QLabel
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        # 设置布局
        self.setLayout(layout)
