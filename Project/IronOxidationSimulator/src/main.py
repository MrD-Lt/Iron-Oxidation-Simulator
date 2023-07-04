import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QVBoxLayout, QLabel, QWidget, QAction
import os
import subprocess

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setFixedSize(1024, 768)

        # Create a menubar
        self.menu = self.menuBar()

        # Add menu items
        self.info_menu = self.menu.addMenu("信息")

        # Create actions for menu items
        self.show_welcome_action = QAction("显示欢迎", self)
        self.show_welcome_action.triggered.connect(self.show_welcome)

        # Add actions to menu items
        self.info_menu.addAction(self.show_welcome_action)

        self.setWindowTitle("主窗口")

    def show_welcome(self):
        self.welcome_window = WelcomeWindow(self)
        self.welcome_window.show()

class WelcomeWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 使用uic模块动态加载ui文件
        uic.loadUi('ui/Welcome.ui', self)

        # 设置窗口标题
        self.setWindowTitle("Welcome!")


        # 将退出按钮与close方法连接
        self.ExitButton.clicked.connect(self.close)

        # 连接Manual按钮的clicked信号到open_pdf_manual方法
        self.Manual.clicked.connect(self.open_pdf_manual)

    def open_pdf_manual(self):
        pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "manual.pdf")
        if not os.path.isfile(pdf_path):
            QMessageBox.critical(self, "File Not Found",
                                 "The manual file does not exist.  Please check the GitHub page or reinstall the "
                                 "software.",
                                 QMessageBox.Ok)
            return
        if sys.platform.startswith('darwin'):  # macOS
            subprocess.call(('open', pdf_path))
        elif sys.platform.startswith('linux'):  # Linux
            subprocess.call(('xdg-open', pdf_path))
        elif sys.platform.startswith('win32'):  # Windows
            os.startfile(pdf_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
