import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

import os
import subprocess


class WelcomeWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 使用uic模块动态加载ui文件
        uic.loadUi('ui/Welcome.ui', self)

        # 设置窗口标题
        self.setWindowTitle("Welcome!")

        # 显示软件名称

        # 显示日期和版本号

        # 将确认按钮与open_main_window方法连接
        self.EntryButton.clicked.connect(self.open_main_window)

        # 将退出按钮与close方法连接
        self.ExitButton.clicked.connect(self.close)

        # 连接Manual按钮的clicked信号到open_pdf_manual方法
        self.Manual.clicked.connect(self.open_pdf_manual)

    def open_main_window(self):
        # 创建主窗口
        # 这里我们没有真正的主窗口，所以我们只创建了一个空的QMainWindow对象
        self.main_window = QMainWindow()
        self.main_window.show()
        self.close()

    def open_pdf_manual(self):
        pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "manual.pdf")
        if sys.platform.startswith('darwin'):  # macOS
            subprocess.call(('open', pdf_path))
        elif sys.platform.startswith('linux'):  # linux
            subprocess.call(('xdg-open', pdf_path))
        elif sys.platform.startswith('win32'):  # Windows
            os.startfile(pdf_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec_())
