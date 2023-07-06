from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal, QObject
import sys
from gui.settings_window import SettingsWindow
from gui.input_window import InputWindow
from gui.button_area import ButtonArea
from gui.help_window import HelpWindow



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 布局设置
        self.setFixedSize(1024, 768)

        # 创建菜单栏
        self.menu = self.menuBar()

        # 功能选择
        self.settings = Settings()

        self.func_menu = self.menu.addMenu("Feature selections")
        self.func_menu.addAction("Option1", self.select_option1)
        self.func_menu.addAction("option2", self.select_option2)
        self.func_menu.addAction("option3", self.select_option3)
        self.func_menu.addAction("option4", self.select_option4)
        # TODO: 根据需要添加更多的选项

        # 输入设置
        self.input_menu = self.menu.addMenu("Input settings")
        self.input_menu.addAction("Manual Input", self.select_option5)
        self.input_menu.addAction("Import File", self.select_option6)

        # 是否保存内容
        self.save_menu = self.menu.addMenu("Save settings")
        self.save_menu.addAction("Yes", self.select_option7)
        self.save_menu.addAction("No", self.select_option8)

        # 帮助
        self.help_menu = self.menu.addMenu("Help")
        self.help_menu.addAction("Info and Help", self.open_help)

        # 联系
        self.help_menu = self.menu.addMenu("Contact with developer")
        self.help_menu.addAction("Github", self.open_contact)
        self.help_menu.addAction("Email", self.open_contact)
        self.help_menu.addAction("Website", self.open_contact)

        # 创建其他部件
        self.settings_window = SettingsWindow(self)
        self.input_window = InputWindow(self)
        self.button_area = ButtonArea(self)

        # 检查Input按钮
        self.settings.settings_changed.connect(self.check_calculate_button_state)
        self.input_window.input_changed.connect(self.check_calculate_button_state)

        self.check_calculate_button_state()  # 检查 "开始计算" 按钮的状态

        # Create a central widget to hold the layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建布局并添加组件
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.settings_window)
        self.layout.addWidget(self.input_window)
        self.layout.addWidget(self.button_area)
        self.central_widget.setLayout(self.layout)

    def check_calculate_button_state(self):
        # 如果有文本输入并且选择的功能不为 "None"，则启用 "开始计算" 按钮
        has_input = self.input_window.manual_input_text.toPlainText() or self.input_window.file_path_label.text()
        func_selected = self.settings.func_current_option != "None"
        self.button_area.calculate_button.setEnabled(bool(has_input) and func_selected)

    def placeholder(self):
        pass  # 占位函数

    def select_option1(self):
        self.settings.set_func_option("Option1")

    def select_option2(self):
        self.settings.set_func_option("Option2")

    def select_option3(self):
        self.settings.set_func_option("Option3")

    def select_option4(self):
        self.settings.set_func_option("Option4")

    def select_option5(self):
        self.settings.set_input_option("Manual Input")

    def select_option6(self):
        self.settings.set_input_option("Import File")

    def select_option7(self):
        self.settings.set_save_option("Yes")

    def select_option8(self):
        self.settings.set_save_option("No")

    def open_help(self):
        # 创建一个 HelpWindow 实例并显示它
        self.help_window = HelpWindow(self)
        self.help_window.show()

    def open_contact(self):
        pass


class Settings(QObject):
    settings_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.func_current_option = "None"
        self.input_current_option = "None"
        self.save_current_option = "No"

    def set_func_option(self, option):
        self.func_current_option = option
        self.settings_changed.emit()

    def set_input_option(self, option):
        self.input_current_option = option
        self.settings_changed.emit()

    def set_save_option(self, option):
        self.save_current_option = option
        self.settings_changed.emit()

    def reset(self):
        self.save_current_option = "No"
        self.input_current_option = "None"
        self.func_current_option = "None"
        self.settings_changed.emit()


if __name__ == "__main__":
    with open("ui/style.qss") as f:
        qss = f.read()
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
